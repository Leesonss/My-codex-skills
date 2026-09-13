#!/usr/bin/env python3
"""Prepare and verify Markdown-to-Word workflows with live Zotero citations."""

from __future__ import annotations

import argparse
import configparser
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections import Counter, defaultdict
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Iterable
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile


TOOL_VERSION = "0.5.1"
SCHEMA_VERSION = 5
ZOTERO_BASE = os.environ.get("ZOTERO_LOCAL_BASE_URL", "http://127.0.0.1:23119")
ODF_SCAN_ID = "rtf-odf-scan-for-zotero@mystery-lab.com"
BBT_ID = "better-bibtex@iris-advies.com"
API_PAGE_SIZE = 100
try:
    API_WORKERS = max(1, min(8, int(os.environ.get("ZOTERO_INDEX_WORKERS", "6"))))
except ValueError:
    API_WORKERS = 6
IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp", ".svg"
}
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W = "{" + W_NS + "}"
M = "{" + M_NS + "}"
CONTENT_PART_RE = re.compile(
    r"^word/(?:document|footnotes|endnotes|comments|header\d+|footer\d+)\.xml$"
)
ITEM_URI_RE = re.compile(r"/items/([A-Z0-9]{8})(?:\b|[/?#])", re.I)
DELIVERY_STAGES = {
    "prepared",
    "waiting_for_delivery_components",
    "waiting_for_delivery_canary",
    "waiting_for_scan",
    "waiting_for_word_refresh",
    "verified",
    "failed",
}
CANARY_ITEM_TYPES = {
    "journalArticle", "book", "bookSection", "conferencePaper", "report", "thesis",
}


class WorkflowError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def payload_fingerprint(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temp.write_text(content, encoding="utf-8")
        os.replace(temp, path)
    finally:
        safe_unlink(temp)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_write(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def default_cache_dir() -> Path:
    root = os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()
    return Path(root) / "Codex" / "markdown-to-zotero-word"


def safe_is_file(path: Path | None) -> bool:
    if not path:
        return False
    try:
        return path.is_file()
    except OSError:
        return False


def probe_file(path: Path | None) -> tuple[str, str | None]:
    if not path:
        return "missing", None
    try:
        return ("available", None) if path.is_file() else ("missing", None)
    except OSError as exc:
        return "unknown", str(exc)


def executable_signature(path: Path | None) -> dict[str, Any] | None:
    if not safe_is_file(path):
        return None
    try:
        stat = path.stat()
        resolved = path.resolve()
    except OSError:
        return None
    return {
        "path": str(resolved),
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }


def registry_app_path(executable: str) -> Path | None:
    if os.name != "nt":
        return None
    try:
        import winreg
    except ImportError:
        return None
    subkey = rf"Software\Microsoft\Windows\CurrentVersion\App Paths\{executable}"
    for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for flags in (0, getattr(winreg, "KEY_WOW64_64KEY", 0), getattr(winreg, "KEY_WOW64_32KEY", 0)):
            try:
                with winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ | flags) as key:
                    value, _ = winreg.QueryValueEx(key, None)
                    candidate = Path(value.strip('"'))
                    if safe_is_file(candidate):
                        return candidate
            except OSError:
                continue
    return None


def find_executable(name: str, env_name: str, candidates: Iterable[Path]) -> Path | None:
    configured = os.environ.get(env_name)
    if configured:
        configured_path = Path(configured.strip('"'))
        if safe_is_file(configured_path):
            return configured_path
        configured_command = shutil.which(configured)
        if configured_command:
            return Path(configured_command)
    located = shutil.which(name)
    if located:
        return Path(located)
    registered = registry_app_path(name)
    if registered:
        return registered
    for candidate in candidates:
        if safe_is_file(candidate):
            return candidate
    return None


def pandoc_version(path: Path | None) -> str | None:
    if not path:
        return None
    try:
        proc = subprocess.run(
            [str(path), "--version"], capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=10, check=False
        )
    except OSError:
        return None
    first = proc.stdout.splitlines()[0] if proc.returncode == 0 and proc.stdout else ""
    return first.removeprefix("pandoc ").strip() or None


def cached_component_path(profile: dict[str, Any] | None, component: str) -> Path | None:
    try:
        entry = profile["components"][component]
        raw = (entry.get("signature") or {}).get("path") or entry.get("path")
    except (KeyError, TypeError):
        return None
    return Path(raw) if raw else None


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        if not path.is_file():
            return None, None
        value = json.loads(path.read_text(encoding="utf-8"))
        return (value, None) if isinstance(value, dict) else (None, f"Expected an object in {path}")
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"Cannot read {path}: {exc}"


def glob_files(root: Path, patterns: Iterable[str]) -> list[Path]:
    found: list[Path] = []
    try:
        if not root.is_dir():
            return found
        for pattern in patterns:
            found.extend(candidate for candidate in root.glob(pattern) if safe_is_file(candidate))
    except OSError:
        return found
    return found


def discover_pandoc(profile: dict[str, Any] | None) -> Path | None:
    executable = "pandoc.exe" if os.name == "nt" else "pandoc"
    explicit = find_executable(executable, "PANDOC", [])
    if explicit:
        return explicit

    candidates: list[Path] = []
    cached = cached_component_path(profile, "pandoc")
    if cached:
        candidates.append(cached)
        candidates.extend(glob_files(cached.parent.parent, [f"pandoc*/{executable}"]))

    local_appdata = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    program_files = Path(os.environ.get("ProgramFiles", "C:/Program Files"))
    program_files_x86 = Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)"))
    candidates.extend([
        local_appdata / "Pandoc" / executable,
        local_appdata / "Microsoft" / "WinGet" / "Links" / executable,
        program_files / "Pandoc" / executable,
        program_files_x86 / "Pandoc" / executable,
        Path.home() / "scoop" / "apps" / "pandoc" / "current" / executable,
    ])

    search_roots: list[Path] = []
    configured_roots = os.environ.get("PANDOC_SEARCH_ROOTS", "")
    search_roots.extend(Path(item) for item in configured_roots.split(os.pathsep) if item)
    search_roots.append(Path.cwd() / "tools")
    if cached:
        search_roots.append(cached.parent.parent)
    for root in dict.fromkeys(search_roots):
        candidates.extend(glob_files(root, [executable, f"pandoc*/{executable}"]))

    if not any(safe_is_file(candidate) for candidate in candidates) and os.name == "nt":
        # Last-resort, version-agnostic discovery under one drive-level tool folder.
        for anchor in dict.fromkeys(filter(None, (Path.cwd().anchor, Path.home().anchor))):
            candidates.extend(glob_files(Path(anchor), [f"*/tools/pandoc*/{executable}"]))

    available: list[Path] = []
    for candidate in candidates:
        if not safe_is_file(candidate):
            continue
        try:
            available.append(candidate.resolve())
        except OSError:
            continue
    available = list(dict.fromkeys(available))
    scored: list[tuple[tuple[int, ...], int, Path]] = []
    for candidate in available:
        version = pandoc_version(candidate) or ""
        version_key = tuple(int(part) for part in re.findall(r"\d+", version)[:4])
        try:
            mtime = candidate.stat().st_mtime_ns
        except OSError:
            mtime = 0
        scored.append((version_key, mtime, candidate))
    return max(scored, default=((), 0, None))[2]


def registry_word_startup_paths() -> list[Path]:
    if os.name != "nt":
        return []
    try:
        import winreg
    except ImportError:
        return []
    paths: list[Path] = []
    for version in ("17.0", "16.0", "15.0", "14.0"):
        subkey = rf"Software\Microsoft\Office\{version}\Word\Options"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey, 0, winreg.KEY_READ) as key:
                value, _ = winreg.QueryValueEx(key, "STARTUP-PATH")
                if value:
                    paths.append(Path(os.path.expandvars(str(value).strip('"'))))
        except OSError:
            continue
    return paths


def discover_word_addin(profile: dict[str, Any] | None) -> tuple[Path | None, str, str | None]:
    candidates: list[Path] = []
    configured = os.environ.get("ZOTERO_WORD_ADDIN")
    if configured:
        candidates.append(Path(configured.strip('"')))
    cached = cached_component_path(profile, "word_addin")
    if cached:
        candidates.append(cached)
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(Path(appdata) / "Microsoft" / "Word" / "STARTUP" / "Zotero.dotm")
    for startup in registry_word_startup_paths():
        candidates.append(startup / "Zotero.dotm")

    unknown: tuple[Path, str] | None = None
    for candidate in dict.fromkeys(candidates):
        state, error = probe_file(candidate)
        if state == "available":
            return candidate, state, None
        if state == "unknown" and unknown is None:
            unknown = (candidate, error or "Access failed")
    if unknown:
        return unknown[0], "unknown", unknown[1]
    return (candidates[0] if candidates else None), "missing", None


def zotero_profile() -> tuple[Path | None, str | None]:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        return None, "APPDATA is unavailable"
    ini = Path(appdata) / "Zotero" / "Zotero" / "profiles.ini"
    try:
        parser = configparser.RawConfigParser()
        with ini.open("r", encoding="utf-8") as handle:
            parser.read_file(handle)
        sections = [s for s in parser.sections() if s.lower().startswith("profile")]
        selected = next((s for s in sections if parser.getboolean(s, "Default", fallback=False)), None)
        selected = selected or (sections[0] if sections else None)
        if not selected:
            return None, f"No profile entry in {ini}"
        raw = parser.get(selected, "Path")
        path = Path(raw)
        if parser.getboolean(selected, "IsRelative", fallback=True):
            path = ini.parent / path
        return path.resolve(), None
    except (OSError, configparser.Error) as exc:
        return None, f"Cannot read Zotero profile: {exc}"


def zotero_data_dir(profile: Path | None) -> Path | None:
    configured = os.environ.get("ZOTERO_DATA_DIR")
    if configured:
        return Path(configured.strip('"')).expanduser()
    if profile:
        prefs = profile / "prefs.js"
        try:
            text = prefs.read_text(encoding="utf-8", errors="replace")
            match = re.search(
                r'user_pref\("extensions\.zotero\.dataDir",\s*"((?:\\.|[^"\\])*)"\)',
                text,
            )
            if match:
                try:
                    return Path(json.loads('"' + match.group(1) + '"'))
                except json.JSONDecodeError:
                    return Path(match.group(1).replace("\\\\", "\\"))
        except OSError:
            pass
    return Path.home() / "Zotero"


def find_zotero_database(profile: Path | None) -> Path | None:
    data_dir = zotero_data_dir(profile)
    candidates = [
        data_dir / "zotero.sqlite" if data_dir else None,
        Path.home() / "Zotero" / "zotero.sqlite",
    ]
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(Path(appdata) / "Zotero" / "Zotero" / "zotero.sqlite")
    for candidate in dict.fromkeys(item for item in candidates if item):
        if safe_is_file(candidate):
            return candidate
    return None


def sqlite_key_index(
    profile: Path | None,
    libraries: list[dict[str, str]],
    expected_versions: dict[str, str | None],
) -> tuple[dict[str, list[dict[str, str]]], dict[str, dict[str, str]], dict[str, Any]] | None:
    """Read current citation keys from a safe, immutable Zotero DB snapshot.

    The database path and schema are treated as optional capabilities. Any
    ambiguity, active WAL, schema drift, or version mismatch returns ``None``
    so the caller can use the public local API instead.
    """
    database = find_zotero_database(profile)
    if not database:
        return None

    def snapshot_signature() -> dict[str, tuple[int, int]] | None:
        signature: dict[str, tuple[int, int]] = {}
        try:
            for candidate in (database, Path(str(database) + "-wal"), Path(str(database) + "-journal")):
                if candidate.is_file():
                    stat = candidate.stat()
                    signature[candidate.name] = (stat.st_size, stat.st_mtime_ns)
            return signature
        except OSError:
            return None

    before = snapshot_signature()
    if not before:
        return None
    for suffix in ("-wal", "-journal"):
        state = before.get(database.name + suffix)
        if state and state[0] > 0:
            return None
    try:
        uri = "file:" + database.as_posix() + "?mode=ro&immutable=1"
        connection = sqlite3.connect(uri, uri=True, timeout=1)
        connection.execute("PRAGMA query_only=ON")
        table_names = {
            row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        required_tables = {
            "libraries", "items", "itemData", "itemDataValues", "fields",
            "itemTypes", "deletedItems", "groups",
        }
        if not required_tables.issubset(table_names):
            connection.close()
            return None
        field_rows = connection.execute(
            "SELECT fieldID, fieldName FROM fields WHERE fieldName IN ('citationKey', 'title')"
        ).fetchall()
        field_ids = {name: field_id for field_id, name in field_rows}
        if "citationKey" not in field_ids:
            connection.close()
            return None

        db_libraries = connection.execute(
            "SELECT libraryID, type, clientVersion FROM libraries"
        ).fetchall()
        db_versions = {str(row[0]): str(row[2]) for row in db_libraries}
        user_library_ids = [int(row[0]) for row in db_libraries if row[1] == "user"]
        group_library_ids = {
            str(group_id): int(library_id)
            for group_id, library_id in connection.execute("SELECT groupID, libraryID FROM groups")
        }
        library_db_ids: dict[str, int] = {}
        for library in libraries:
            logical = f"{library['type']}:{library['id']}"
            if library["type"] == "user":
                if len(user_library_ids) != 1:
                    connection.close()
                    return None
                db_id = user_library_ids[0]
            else:
                db_id = group_library_ids.get(library["id"])
                if db_id is None:
                    connection.close()
                    return None
            if expected_versions.get(logical) != db_versions[str(db_id)]:
                connection.close()
                return None
            library_db_ids[logical] = db_id

        title_id = field_ids.get("title", -1)
        rows = connection.execute(
            """
            SELECT i.itemID, i.key, i.libraryID, cite.value, title.value, itemType.typeName
            FROM items AS i
            JOIN itemTypes AS itemType ON itemType.itemTypeID = i.itemTypeID
            JOIN itemData AS citeData
              ON citeData.itemID = i.itemID AND citeData.fieldID = ?
            JOIN itemDataValues AS cite ON cite.valueID = citeData.valueID
            LEFT JOIN itemData AS titleData
              ON titleData.itemID = i.itemID AND titleData.fieldID = ?
            LEFT JOIN itemDataValues AS title ON title.valueID = titleData.valueID
            LEFT JOIN deletedItems AS deleted ON deleted.itemID = i.itemID
            WHERE deleted.itemID IS NULL AND trim(cite.value) <> ''
            """,
            (field_ids["citationKey"], title_id),
        ).fetchall()
        connection.close()
    except (OSError, sqlite3.Error):
        try:
            connection.close()
        except (UnboundLocalError, sqlite3.Error):
            pass
        return None

    after = snapshot_signature()
    if before != after:
        return None

    names_by_db_id = {
        library_db_ids[f"{library['type']}:{library['id']}"]: library["name"]
        for library in libraries
    }
    logical_by_db_id = {
        library_db_ids[f"{library['type']}:{library['id']}"]: f"{library['type']}:{library['id']}"
        for library in libraries
    }
    records: dict[str, dict[str, str]] = {}
    for _, item_key, db_id, citation_key, title, item_type in rows:
        logical = logical_by_db_id.get(db_id)
        if not logical:
            continue
        library = next(item for item in libraries if f"{item['type']}:{item['id']}" == logical)
        record = {
            "library": names_by_db_id[db_id],
            "library_type": library["type"],
            "library_id": library["id"],
            "item_key": str(item_key),
            "title": title or "",
            "item_type": item_type or "",
            "citation_key": str(citation_key).strip(),
        }
        records[f"{logical}:{item_key}"] = record
    index: dict[str, list[dict[str, str]]] = defaultdict(list)
    for record in records.values():
        index[record["citation_key"]].append({key: value for key, value in record.items() if key != "citation_key"})
    return dict(index), records, {
        "source": "zotero-sqlite",
        "fresh": True,
        "database": str(database),
        "database_signature": after,
        "key_count": len(index),
        "item_count": len(records),
        "library_versions": expected_versions,
    }


def extension_status(profile: Path | None) -> tuple[dict[str, Any], list[str]]:
    result = {
        "better_bibtex": {"id": BBT_ID, "state": "unknown"},
        "odf_docx_scan": {"id": ODF_SCAN_ID, "state": "unknown"},
    }
    warnings: list[str] = []
    if not profile:
        warnings.append("Zotero profile is unavailable; plugin state is unknown")
        return result, warnings
    extensions = profile / "extensions.json"
    try:
        data = json.loads(extensions.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        warnings.append(f"Cannot read {extensions}: {exc}")
        return result, warnings
    addons = [addon for addon in data.get("addons", []) if isinstance(addon, dict)]
    by_id = {addon.get("id"): addon for addon in addons}

    def addon_text(addon: dict[str, Any]) -> str:
        locale = addon.get("defaultLocale") if isinstance(addon.get("defaultLocale"), dict) else {}
        values = [addon.get("id"), addon.get("name"), locale.get("name"), addon.get("path")]
        return " ".join(str(value) for value in values if value).lower()

    def fallback_addon(kind: str) -> dict[str, Any] | None:
        for addon in addons:
            text = addon_text(addon)
            if kind == "better_bibtex" and ("better bibtex" in text or "better-bibtex" in text):
                return addon
            if kind == "odf_docx_scan" and (
                "odf/docx scan" in text or "odf scan" in text or "rtf-odf-scan" in text
            ):
                return addon
        return None

    for key, extension_id in (("better_bibtex", BBT_ID), ("odf_docx_scan", ODF_SCAN_ID)):
        addon = by_id.get(extension_id) or fallback_addon(key)
        if not addon:
            result[key] = {"id": extension_id, "state": "missing"}
        else:
            result[key] = {
                "id": addon.get("id", extension_id),
                "expected_id": extension_id,
                "matched_by": "id" if addon.get("id") == extension_id else "metadata",
                "state": "active" if addon.get("active") else "inactive",
                "version": addon.get("version"),
                "path": addon.get("path"),
            }
    return result, warnings


def http_get(path: str, timeout: int = 8, retries: int = 2) -> tuple[Any, dict[str, str]]:
    request = urllib.request.Request(
        ZOTERO_BASE + path,
        headers={"Zotero-API-Version": "3", "Accept": "application/json"},
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read()
                headers = {key: value for key, value in response.headers.items()}
            if not raw:
                return None, headers
            decoded = raw.decode("utf-8", errors="replace")
            try:
                return json.loads(decoded), headers
            except json.JSONDecodeError:
                return decoded, headers
        except urllib.error.HTTPError as exc:
            retryable = exc.code == 429 or 500 <= exc.code < 600
            if not retryable or attempt >= retries:
                raise
            retry_after = exc.headers.get("Retry-After")
            try:
                delay = min(4.0, max(0.2, float(retry_after))) if retry_after else 0.2 * (2 ** attempt)
            except ValueError:
                delay = 0.2 * (2 ** attempt)
            time.sleep(delay)
        except (OSError, urllib.error.URLError):
            if attempt >= retries:
                raise
            time.sleep(min(4.0, 0.2 * (2 ** attempt)))
    raise WorkflowError(f"HTTP request failed after {retries + 1} attempts: {path}")


def api_probe() -> dict[str, Any]:
    try:
        _, headers = http_get("/api/", timeout=3)
        return {
            "state": "running",
            "version": headers.get("X-Zotero-Version"),
            "api_version": headers.get("Zotero-API-Version"),
            "schema_version": headers.get("Zotero-Schema-Version"),
            "base_url": ZOTERO_BASE,
        }
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        return {"state": "unavailable", "base_url": ZOTERO_BASE, "error": str(exc)}


def stabilized_component(
    current: dict[str, Any], previous: dict[str, Any] | None
) -> dict[str, Any]:
    """Keep compatibility identity stable when inspection is temporarily denied."""
    if not previous:
        return deepcopy(current)
    if current.get("state") == "unknown" and previous.get("state") != "unknown":
        return deepcopy(previous)
    result = deepcopy(current)
    for key, value in list(result.items()):
        old_value = previous.get(key)
        if value is None and old_value is not None:
            result[key] = deepcopy(old_value)
        elif isinstance(value, dict) and isinstance(old_value, dict):
            result[key] = stabilized_component(value, old_value)
    return result


def compatibility_components(
    components: dict[str, dict[str, Any]], old: dict[str, Any] | None
) -> dict[str, dict[str, Any]]:
    old_components = (old or {}).get("last_known_components") or (old or {}).get("components") or {}
    return {
        name: stabilized_component(component, old_components.get(name))
        for name, component in components.items()
    }


def doctor(cache_dir: Path, write_profile: bool = True) -> dict[str, Any]:
    profile_path = cache_dir / "capabilities.json"
    old, old_error = load_json(profile_path)
    program_files = Path(os.environ.get("ProgramFiles", "C:/Program Files"))
    program_files_x86 = Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)"))
    pandoc = discover_pandoc(old)
    local_appdata = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    zotero = find_executable(
        "zotero.exe" if os.name == "nt" else "zotero", "ZOTERO_EXE",
        [
            local_appdata / "Zotero" / "zotero.exe",
            program_files / "Zotero" / "zotero.exe",
            program_files_x86 / "Zotero" / "zotero.exe",
            *glob_files(program_files, ["Zotero*/zotero.exe"]),
            *glob_files(program_files_x86, ["Zotero*/zotero.exe"]),
        ],
    )
    word = find_executable(
        "WINWORD.EXE" if os.name == "nt" else "winword", "WORD_EXE",
        [
            program_files / "Microsoft Office" / "root" / "Office16" / "WINWORD.EXE",
            program_files_x86 / "Microsoft Office" / "root" / "Office16" / "WINWORD.EXE",
            *glob_files(program_files / "Microsoft Office", ["*/WINWORD.EXE", "*/root/*/WINWORD.EXE"]),
            *glob_files(program_files_x86 / "Microsoft Office", ["*/WINWORD.EXE", "*/root/*/WINWORD.EXE"]),
        ],
    )
    profile, profile_error = zotero_profile()
    extensions, extension_warnings = extension_status(profile)
    addin, addin_state, addin_error = discover_word_addin(old)
    api = api_probe()
    warnings = extension_warnings
    warnings.extend(error for error in (old_error, profile_error) if error)
    if addin_error:
        warnings.append(f"Cannot inspect Word Zotero add-in {addin}: {addin_error}")
    pandoc_v = pandoc_version(pandoc)
    if pandoc and not pandoc_v:
        warnings.append(f"Pandoc was found but could not be executed: {pandoc}")
    components = {
        "pandoc": {"state": "available" if pandoc and pandoc_v else "missing", "version": pandoc_v, "signature": executable_signature(pandoc)},
        "zotero": {"state": "available" if zotero else "missing", "signature": executable_signature(zotero), "api": api, "profile": str(profile) if profile else None},
        "word": {"state": "available" if word else "missing", "signature": executable_signature(word)},
        "word_addin": {"state": addin_state, "path": str(addin) if addin else None, "signature": executable_signature(addin)},
        **extensions,
    }
    fingerprint_components = compatibility_components(components, old)
    fingerprints = {
        "overall": payload_fingerprint(fingerprint_components),
        "converter": payload_fingerprint({
            "schema_version": SCHEMA_VERSION,
            "tool_version": TOOL_VERSION,
            "pandoc": fingerprint_components["pandoc"],
        }),
        "citation_index": payload_fingerprint({
            "schema_version": SCHEMA_VERSION,
            "tool_version": TOOL_VERSION,
            "zotero_profile": fingerprint_components["zotero"].get("profile"),
            "zotero_api_version": api.get("version"),
            "zotero_schema_version": api.get("schema_version"),
            "better_bibtex": fingerprint_components["better_bibtex"],
        }),
        "delivery": payload_fingerprint({
            "schema_version": SCHEMA_VERSION,
            "tool_version": TOOL_VERSION,
            "zotero": fingerprint_components["zotero"],
            "word": fingerprint_components["word"],
            "word_addin": fingerprint_components["word_addin"],
            "better_bibtex": fingerprint_components["better_bibtex"],
            "odf_docx_scan": fingerprint_components["odf_docx_scan"],
        }),
    }
    fingerprint = fingerprints["overall"]
    change_reasons: list[str] = []
    if old and old.get("fingerprint") != fingerprint:
        change_reasons.append("components")
    if old and old.get("tool_version") != TOOL_VERSION:
        change_reasons.append("workflow")
    if old and old.get("schema_version") != SCHEMA_VERSION:
        change_reasons.append("schema")
    changed = bool(change_reasons)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "checked_at": now_iso(),
        "fingerprint": fingerprint,
        "fingerprints": fingerprints,
        "profile_changed": changed,
        "profile_change_reasons": change_reasons,
        "components": components,
        "last_known_components": fingerprint_components,
        "ready": {
            "prepare": bool(pandoc and pandoc_v),
            "key_validation": api.get("state") == "running",
            "delivery": all([
                pandoc and pandoc_v,
                zotero,
                word,
                addin_state == "available",
                api.get("state") == "running",
                extensions["better_bibtex"].get("state") == "active",
                extensions["odf_docx_scan"].get("state") == "active",
            ]),
        },
        "warnings": warnings,
    }
    if write_profile:
        try:
            atomic_json(profile_path, payload)
            payload["profile_path"] = str(profile_path)
        except OSError as exc:
            payload["warnings"].append(f"Capability profile was not written: {exc}")
    return payload


def delivery_blockers(capabilities: dict[str, Any]) -> list[str]:
    components = capabilities.get("components", {})
    blockers: list[str] = []
    required_states = {
        "pandoc": "available",
        "zotero": "available",
        "word": "available",
        "word_addin": "available",
        "better_bibtex": "active",
        "odf_docx_scan": "active",
    }
    for name, expected in required_states.items():
        actual = (components.get(name) or {}).get("state")
        if actual != expected:
            blockers.append(f"{name}:{actual or 'unknown'}")
    api_state = ((components.get("zotero") or {}).get("api") or {}).get("state")
    if api_state != "running":
        blockers.append(f"zotero_api:{api_state or 'unknown'}")
    return blockers


def api_libraries() -> list[dict[str, str]]:
    libraries = [{"type": "user", "id": "0", "base": "/api/users/0", "name": "My Library"}]
    try:
        groups, _ = http_get("/api/users/0/groups?limit=100")
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return libraries
    if not isinstance(groups, list):
        return libraries
    for group in groups or []:
        if not isinstance(group, dict):
            continue
        data = group.get("data", group)
        if not isinstance(data, dict):
            continue
        group_id = data.get("id") or group.get("id")
        if group_id is not None:
            libraries.append({
                "type": "group", "id": str(group_id),
                "base": f"/api/groups/{group_id}", "name": data.get("name", f"Group {group_id}"),
            })
    return libraries


def library_version(base: str) -> str | None:
    _, headers = http_get(f"{base}/items?itemType=-attachment&limit=1&format=json")
    return headers.get("Last-Modified-Version")


def fetch_library_items(base: str) -> list[dict[str, Any]]:
    def fetch_page(start: int) -> tuple[list[dict[str, Any]], dict[str, str]]:
        path = (
            f"{base}/items?itemType=-attachment&limit={API_PAGE_SIZE}"
            f"&start={start}&format=json"
        )
        page, headers = http_get(path, timeout=30)
        if page is None:
            page = []
        if not isinstance(page, list):
            raise WorkflowError(f"Unexpected Zotero item response for {base} at start={start}")
        return page, headers

    first_page, headers = fetch_page(0)
    raw_total = headers.get("Total-Results")
    if raw_total is None:
        items = list(first_page)
        start = len(first_page)
        while first_page and len(first_page) == API_PAGE_SIZE:
            first_page, _ = fetch_page(start)
            items.extend(first_page)
            start += len(first_page)
        return items

    total = int(raw_total)
    starts = list(range(API_PAGE_SIZE, total, API_PAGE_SIZE))
    items = list(first_page)
    if starts:
        workers = min(API_WORKERS, len(starts))
        with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="zotero-index") as pool:
            for page, _ in pool.map(fetch_page, starts):
                items.extend(page)
    if len(items) != total:
        raise WorkflowError(
            f"Zotero library changed or returned an incomplete snapshot for {base}: "
            f"expected {total} items, received {len(items)}"
        )
    return items


def refresh_key_index(
    cache_dir: Path,
    force: bool = False,
    capability_fingerprint: str | None = None,
) -> tuple[dict[str, list[dict[str, str]]], dict[str, Any]]:
    started = perf_counter()
    cache_path = cache_dir / "citation-key-index.json"
    cached, cache_error = load_json(cache_path)
    cached_keys = cached.get("keys") if isinstance(cached, dict) else None
    cache_is_usable = isinstance(cached_keys, dict) and bool(cached_keys)

    def stale_cache(exc: Exception) -> tuple[dict[str, list[dict[str, str]]], dict[str, Any]]:
        if cache_is_usable:
            return cached_keys, {
                "source": "stale-cache",
                "fresh": False,
                "cache_path": str(cache_path),
                "warning": f"Zotero refresh failed; using cached keys: {exc}",
                "key_count": len(cached_keys),
                "duration_seconds": round(perf_counter() - started, 3),
            }
        raise WorkflowError(f"Zotero API unavailable and no key cache exists: {exc}") from exc

    try:
        libraries = api_libraries()
        versions: dict[str, str | None] = {}
        for library in libraries:
            versions[f"{library['type']}:{library['id']}"] = library_version(library["base"])
        cache_matches = (
            cache_is_usable
            and all(versions.values())
            and cached.get("schema_version") == SCHEMA_VERSION
            and cached.get("library_versions") == versions
            and (
                not capability_fingerprint
                or cached.get("capability_fingerprint") == capability_fingerprint
            )
        )
        if not force and cache_matches:
            return cached_keys, {
                "source": "cache", "fresh": True, "cache_path": str(cache_path),
                "key_count": len(cached_keys), "library_versions": versions,
                "duration_seconds": round(perf_counter() - started, 3),
            }

        profile, _ = zotero_profile()
        sqlite_result = sqlite_key_index(profile, libraries, versions)
        if sqlite_result:
            sqlite_keys, sqlite_records, sqlite_meta = sqlite_result
            payload = {
                "schema_version": SCHEMA_VERSION,
                "tool_version": TOOL_VERSION,
                "generated_at": now_iso(),
                "capability_fingerprint": capability_fingerprint,
                "library_versions": versions,
                "item_count": len(sqlite_records),
                "fetched_item_count": len(sqlite_records),
                "records": sqlite_records,
                "keys": sqlite_keys,
            }
            atomic_json(cache_path, payload)
            return sqlite_keys, {
                **sqlite_meta,
                "cache_path": str(cache_path),
                "duration_seconds": round(perf_counter() - started, 3),
            }

        for attempt in range(2):
            index: dict[str, list[dict[str, str]]] = defaultdict(list)
            records: dict[str, dict[str, str]] = {}
            item_count = 0
            fetched_item_count = 0
            for library in libraries:
                items = fetch_library_items(library["base"])
                fetched_item_count += len(items)
                for item in items:
                    data = item.get("data", item)
                    key = (data.get("citationKey") or "").strip()
                    if not key:
                        continue
                    item_count += 1
                    record = {
                        "library": library["name"],
                        "library_type": library["type"],
                        "library_id": library["id"],
                        "item_key": data.get("key", ""),
                        "title": data.get("title", ""),
                        "item_type": data.get("itemType", ""),
                        "citation_key": key,
                    }
                    records[f"{library['type']}:{library['id']}:{record['item_key']}"] = record
                    index[key].append({field: value for field, value in record.items() if field != "citation_key"})
            final_versions = {
                f"{library['type']}:{library['id']}": library_version(library["base"])
                for library in libraries
            }
            if final_versions == versions:
                break
            if attempt == 0:
                versions = final_versions
                continue
            raise WorkflowError("Zotero library changed twice while the citation-key index was refreshing")
    except (OSError, urllib.error.URLError, json.JSONDecodeError, ValueError, WorkflowError) as exc:
        return stale_cache(exc)

    payload = {
        "schema_version": SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "generated_at": now_iso(),
        "capability_fingerprint": capability_fingerprint,
        "library_versions": versions,
        "item_count": item_count,
        "fetched_item_count": fetched_item_count,
        "records": records,
        "keys": dict(index),
    }
    atomic_json(cache_path, payload)
    return payload["keys"], {
        "source": "zotero-api", "fresh": True, "cache_path": str(cache_path),
        "key_count": len(index), "item_count": item_count,
        "fetched_item_count": fetched_item_count,
        "library_versions": versions,
        "workers": API_WORKERS,
        "duration_seconds": round(perf_counter() - started, 3),
        **({"cache_warning": cache_error} if cache_error else {}),
    }


def bibtex_index(path: Path) -> dict[str, list[dict[str, str]]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(r"(?mi)^\s*@(?!comment\b|string\b|preamble\b)[A-Za-z]+\s*[({]\s*([^,\s]+)\s*,")
    index: dict[str, list[dict[str, str]]] = defaultdict(list)
    for match in pattern.finditer(text):
        index[match.group(1)].append({"library": str(path), "item_key": "", "title": ""})
    return dict(index)


def run_pandoc(pandoc: Path, args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        [str(pandoc), *args], cwd=str(cwd) if cwd else None,
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    if proc.returncode != 0:
        raise WorkflowError(f"Pandoc failed ({proc.returncode}): {proc.stderr.strip()}")
    return proc


def walk_ast(node: Any, stats: dict[str, Any]) -> None:
    if isinstance(node, dict):
        node_type = node.get("t")
        if node_type == "Cite":
            stats["citation_clusters"] += 1
            for citation in node.get("c", [[], []])[0]:
                citation_id = citation.get("citationId", "")
                if citation_id:
                    stats["citation_ids"].append(citation_id)
        elif node_type == "Header":
            stats["headings"] += 1
        elif node_type == "Table":
            stats["tables"] += 1
        elif node_type == "Math":
            stats["math_nodes"] += 1
        elif node_type == "Image":
            try:
                stats["image_targets"].append(node["c"][2][0])
            except (KeyError, IndexError, TypeError):
                pass
        for value in node.values():
            walk_ast(value, stats)
    elif isinstance(node, list):
        for value in node:
            walk_ast(value, stats)


def inspect_markdown(pandoc: Path, path: Path) -> dict[str, Any]:
    proc = run_pandoc(pandoc, ["--from=markdown+citations", "--to=json", str(path)], cwd=path.parent)
    ast = json.loads(proc.stdout)
    stats: dict[str, Any] = {
        "citation_clusters": 0,
        "citation_ids": [],
        "headings": 0,
        "tables": 0,
        "math_nodes": 0,
        "image_targets": [],
    }
    walk_ast(ast, stats)
    counts = Counter(stats.pop("citation_ids"))
    stats["citation_occurrences"] = sum(counts.values())
    stats["unique_citation_keys"] = len(counts)
    stats["citation_counts"] = dict(sorted(counts.items()))
    stats["slash_keys"] = sorted(key for key in counts if "/" in key)
    return stats


def resolve_media(target: str, roots: list[Path]) -> tuple[Path | None, str | None]:
    if re.match(r"^(?:https?|data):", target, re.I):
        return None, "remote"
    cleaned = urllib.parse.unquote(target.strip("<>"))
    candidate = Path(cleaned)
    if candidate.is_absolute() and safe_is_file(candidate):
        try:
            return candidate.resolve(), None
        except OSError:
            return None, "unreadable"
    for root in roots:
        try:
            direct = root / candidate
            if safe_is_file(direct):
                return direct.resolve(), None
        except OSError:
            continue
    basename = candidate.name
    matches: list[Path] = []
    for root in roots:
        try:
            matches.extend(item.resolve() for item in root.rglob(basename) if safe_is_file(item))
        except OSError:
            continue
    unique = list(dict.fromkeys(matches))
    if len(unique) == 1:
        return unique[0], None
    if len(unique) > 1:
        return None, "ambiguous"
    return None, "missing"


def validate_media_targets(
    targets: Iterable[str], roots: list[Path], allow_remote: bool, allow_missing: bool = False
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for target in dict.fromkeys(targets):
        resolved, state = resolve_media(target, roots)
        if state == "remote":
            finding = {"target": target, "state": "remote"}
            findings.append(finding)
            if not allow_remote:
                raise WorkflowError(
                    "Remote media requires explicit allowance and network access: " + target
                )
            continue
        if not resolved:
            finding = {"target": target, "state": state or "missing"}
            findings.append(finding)
            if not allow_missing:
                raise WorkflowError(f"Unresolved Markdown image: {target} ({state or 'missing'})")
            continue
        findings.append({"target": target, "state": "resolved", "path": str(resolved)})
    return findings


def normalize_obsidian(text: str, roots: list[Path]) -> tuple[str, list[dict[str, str]]]:
    findings: list[dict[str, str]] = []
    pattern = re.compile(r"!\[\[([^\]]+)\]\]")

    def replace(match: re.Match[str]) -> str:
        inner = match.group(1)
        target, _, alias = inner.partition("|")
        target = target.strip()
        if Path(target).suffix.lower() not in IMAGE_EXTENSIONS:
            findings.append({"target": target, "state": "unsupported-embed"})
            return match.group(0)
        resolved, state = resolve_media(target, roots)
        if not resolved:
            findings.append({"target": target, "state": state or "missing"})
            return match.group(0)
        label = alias.strip() or resolved.stem
        findings.append({"target": target, "state": "resolved", "path": str(resolved)})
        return f"![{label}](<{resolved.as_posix()}>)"

    return pattern.sub(replace, text), findings


def docx_parts(archive: ZipFile) -> list[str]:
    return [name for name in archive.namelist() if CONTENT_PART_RE.match(name)]


def word_field_instructions(root: ET.Element) -> list[str]:
    fields: list[str] = []
    stack: list[list[str]] = []
    for node in root.iter():
        if node.tag == W + "fldSimple":
            instruction = node.attrib.get(W + "instr", "").strip()
            if instruction:
                fields.append(instruction)
            continue
        if node.tag == W + "fldChar":
            field_type = node.attrib.get(W + "fldCharType", "")
            if field_type == "begin":
                stack.append([])
            elif field_type == "end" and stack:
                instruction = "".join(stack.pop()).strip()
                if instruction:
                    fields.append(instruction)
            continue
        if node.tag == W + "instrText" and stack:
            stack[-1].append(node.text or "")
    return fields


def field_json(instruction: str, marker: str) -> dict[str, Any] | None:
    match = re.search(re.escape(marker), instruction, re.I)
    if not match:
        return None
    payload = instruction[match.end():].lstrip()
    start = payload.find("{")
    if start < 0:
        return None
    try:
        value, _ = json.JSONDecoder().raw_decode(payload[start:])
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def zotero_field_summary(instructions: Iterable[str]) -> dict[str, Any]:
    citation_fields: list[str] = []
    bibliography_fields: list[str] = []
    preferences: dict[str, Any] | None = None
    item_keys: Counter[str] = Counter()
    unparsable_citations = 0
    for instruction in instructions:
        if re.search(r"ADDIN\s+ZOTERO_ITEM\s+CSL_CITATION", instruction, re.I):
            citation_fields.append(instruction)
            data = field_json(instruction, "CSL_CITATION") or {}
            keys: list[str] = []
            for item in data.get("citationItems", []):
                if not isinstance(item, dict):
                    continue
                values = item.get("uris") or ([item["uri"]] if item.get("uri") else [])
                field_item_keys = {
                    key.upper()
                    for value in values
                    for key in ITEM_URI_RE.findall(str(value))
                }
                keys.extend(sorted(field_item_keys))
            if not keys:
                keys = ITEM_URI_RE.findall(instruction)
            if keys:
                item_keys.update(key.upper() for key in keys)
            else:
                unparsable_citations += 1
        elif re.search(r"ADDIN\s+ZOTERO_BIBL", instruction, re.I):
            bibliography_fields.append(instruction)
        elif re.search(r"ADDIN\s+ZOTERO_PREF_1", instruction, re.I):
            preferences = field_json(instruction, "ZOTERO_PREF_1") or preferences
    return {
        "live_citation_fields": len(citation_fields),
        "live_bibliography_fields": len(bibliography_fields),
        "zotero_item_keys": dict(sorted(item_keys.items())),
        "unparsable_citation_fields": unparsable_citations,
        "zotero_preferences": preferences or {},
    }


def docx_fingerprint(path: Path, expected_keys: Iterable[str] = ()) -> dict[str, Any]:
    try:
        with ZipFile(path) as archive:
            text_paragraphs: list[str] = []
            instructions: list[str] = []
            tables = drawings = math_nodes = paragraphs = hyperlinks = sections = 0
            tracked_insertions = tracked_deletions = 0
            heading_styles: Counter[str] = Counter()
            for name in docx_parts(archive):
                root = ET.fromstring(archive.read(name))
                tables += len(root.findall(f".//{W}tbl"))
                drawings += len(root.findall(f".//{W}drawing")) + len(root.findall(f".//{W}pict"))
                math_nodes += len(root.findall(f".//{M}oMath"))
                paragraphs += len(root.findall(f".//{W}p"))
                hyperlinks += len(root.findall(f".//{W}hyperlink"))
                sections += len(root.findall(f".//{W}sectPr"))
                tracked_insertions += len(root.findall(f".//{W}ins"))
                tracked_deletions += len(root.findall(f".//{W}del"))
                instructions.extend(word_field_instructions(root))
                for paragraph in root.findall(f".//{W}p"):
                    text_paragraphs.append("".join((node.text or "") for node in paragraph.findall(f".//{W}t")))
                    style = paragraph.find(f"./{W}pPr/{W}pStyle")
                    if style is not None:
                        value = style.attrib.get(W + "val", "")
                        if value.lower().startswith("heading") or value.startswith("标题"):
                            heading_styles[value] += 1
            visible_text = "\n".join(text_paragraphs)
            zotero_fields = zotero_field_summary(instructions)
            raw_counts: dict[str, int] = {}
            for key in expected_keys:
                raw_counts[key] = len(re.findall(
                    rf"(?<![A-Za-z0-9_/+-])@{re.escape(key)}(?![A-Za-z0-9_/+-])", visible_text
                ))
            media = {}
            for name in archive.namelist():
                if name.startswith("word/media/") and not name.endswith("/"):
                    media[name] = hashlib.sha256(archive.read(name)).hexdigest()
            return {
                "tables": tables,
                "drawings": drawings,
                "math_nodes": math_nodes,
                "paragraphs": paragraphs,
                "hyperlinks": hyperlinks,
                "sections": sections,
                "tracked_insertions": tracked_insertions,
                "tracked_deletions": tracked_deletions,
                "heading_styles": dict(sorted(heading_styles.items())),
                "media": media,
                **zotero_fields,
                "raw_citation_counts": raw_counts,
                "raw_citation_occurrences": sum(raw_counts.values()),
                "visible_text_sha256": hashlib.sha256(visible_text.encode("utf-8")).hexdigest(),
            }
    except (OSError, BadZipFile, ET.ParseError) as exc:
        raise WorkflowError(f"Cannot inspect DOCX {path}: {exc}") from exc


def structural_differences(
    baseline: dict[str, Any], current: dict[str, Any], allow_bibliography: bool = False
) -> list[str]:
    differences = []
    keys = [
        "tables", "drawings", "math_nodes", "paragraphs", "hyperlinks",
        "sections", "heading_styles", "tracked_insertions", "tracked_deletions",
    ]
    if allow_bibliography:
        keys = [key for key in keys if key not in {"paragraphs", "hyperlinks"}]
    for key in keys:
        if key in baseline and baseline.get(key) != current.get(key):
            differences.append(key)
    baseline_media = Counter((baseline.get("media") or {}).values())
    current_media = Counter((current.get("media") or {}).values())
    if baseline_media != current_media:
        differences.append("media")
    return differences


def report_markdown(title: str, status: str, rows: list[tuple[str, str, str]], metadata: dict[str, Any]) -> str:
    lines = [f"# {title}", "", f"- Status: `{status}`", f"- Generated: `{now_iso()}`"]
    for key, value in metadata.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Checks", "", "| Check | Status | Detail |", "|---|---|---|"])
    for check, check_status, detail in rows:
        safe = str(detail).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {check} | `{check_status}` | {safe} |")
    return "\n".join(lines) + "\n"


def unique_output(path: Path, force: bool) -> None:
    try:
        exists = path.exists()
    except OSError as exc:
        raise WorkflowError(f"Cannot inspect output path {path}: {exc}") from exc
    if exists and not force:
        raise WorkflowError(f"Output already exists: {path}. Choose a new path or pass --force explicitly.")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise WorkflowError(f"Cannot create output directory {path.parent}: {exc}") from exc


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"Cannot read preparation manifest {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise WorkflowError(f"Preparation manifest must contain a JSON object: {path}")
    required = {
        "schema_version", "source", "intermediate_docx", "citations",
        "intermediate_fingerprint",
    }
    missing = sorted(required - set(payload))
    if missing:
        raise WorkflowError("Preparation manifest is missing: " + ", ".join(missing))
    if not isinstance(payload.get("citations"), dict) or not isinstance(
        payload["citations"].get("citation_counts"), dict
    ):
        raise WorkflowError("Preparation manifest has invalid citation statistics")
    if not isinstance(payload.get("intermediate_fingerprint"), dict):
        raise WorkflowError("Preparation manifest has an invalid DOCX fingerprint")
    return payload


def manifest_job(manifest: dict[str, Any]) -> dict[str, Any]:
    job = manifest.get("job")
    if not isinstance(job, dict):
        job = {
            "run_id": "legacy-" + payload_fingerprint(manifest)[:16],
            "requested_mode": manifest.get("mode", "delivery"),
            "current_stage": "prepared",
            "state": "prepared",
            "history": [],
        }
        manifest["job"] = job
    if job.get("current_stage") not in DELIVERY_STAGES:
        job["current_stage"] = "prepared"
    if not isinstance(job.get("history"), list):
        job["history"] = []
    return job


def update_manifest_state(
    path: Path,
    manifest: dict[str, Any],
    state: str,
    detail: str,
    waiting_for: Iterable[str] = (),
) -> None:
    if state not in DELIVERY_STAGES:
        raise WorkflowError(f"Invalid delivery state: {state}")
    job = manifest_job(manifest)
    event = {"at": now_iso(), "state": state, "detail": detail}
    if not job["history"] or any(
        job["history"][-1].get(key) != event[key] for key in ("state", "detail")
    ):
        job["history"].append(event)
    job["current_stage"] = state
    job["state"] = state
    job["waiting_for"] = list(waiting_for)
    atomic_json(path, manifest)


def delivery_canary_status(cache_dir: Path, delivery_fingerprint: str | None) -> dict[str, Any]:
    path = cache_dir / "delivery-test-status.json"
    cached, error = load_json(path)
    passed = bool(
        delivery_fingerprint
        and cached
        and cached.get("status") == "PASS"
        and cached.get("schema_version") == SCHEMA_VERSION
        and cached.get("tool_version") == TOOL_VERSION
        and cached.get("delivery_fingerprint") == delivery_fingerprint
    )
    return {
        "status": "PASS" if passed else "REQUIRED",
        "cache_path": str(path),
        **({"checked_at": cached.get("checked_at")} if passed else {}),
        **({"warning": error} if error else {}),
    }


def expected_zotero_item_counts(manifest: dict[str, Any]) -> Counter[str] | None:
    resolved = (manifest.get("key_validation") or {}).get("resolved_items")
    counts = (manifest.get("citations") or {}).get("citation_counts") or {}
    if not isinstance(resolved, dict) or not counts:
        return None
    expected: Counter[str] = Counter()
    for citation_key, count in counts.items():
        record = resolved.get(citation_key)
        item_key = record.get("item_key") if isinstance(record, dict) else None
        if not item_key:
            return None
        expected[str(item_key).upper()] += int(count)
    return expected


def normalize_style(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    cleaned = value.strip().replace("\\", "/").rstrip("/")
    name = cleaned.rsplit("/", 1)[-1]
    return name[:-4].lower() if name.lower().endswith(".csl") else name.lower()


def normalize_locale(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip().replace("_", "-").lower()


def manifest_binding_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_info = manifest.get("source") or {}
    if source_info.get("path"):
        source_path = Path(source_info["path"])
        if safe_is_file(source_path) and sha256_file(source_path) != source_info.get("sha256"):
            errors.append("source_changed_after_preparation")
    intermediate_info = manifest.get("intermediate_docx") or {}
    if not intermediate_info.get("path"):
        errors.append("intermediate_path_missing")
    else:
        intermediate_path = Path(intermediate_info["path"])
        if not safe_is_file(intermediate_path):
            errors.append("intermediate_docx_missing")
        elif sha256_file(intermediate_path) != intermediate_info.get("sha256"):
            errors.append("intermediate_docx_changed")
    return errors


def evaluate_delivery_docx(
    docx: Path,
    manifest: dict[str, Any],
    require_live: bool = True,
    require_bibliography: bool = False,
    allow_output_mismatch: bool = False,
) -> dict[str, Any]:
    keys = list(manifest["citations"]["citation_counts"])
    current = docx_fingerprint(docx, keys)
    baseline = manifest["intermediate_fingerprint"]
    job = manifest_job(manifest)
    expected_clusters = int(manifest["citations"].get("citation_clusters", 0))
    requested_bibliography = bool(job.get("insert_bibliography"))
    require_bibliography = require_bibliography or requested_bibliography
    differences = structural_differences(
        baseline, current, allow_bibliography=require_bibliography
    )
    rows: list[tuple[str, str, str]] = []

    expected_output = job.get("live_output")
    output_matches = True
    if expected_output:
        try:
            output_matches = Path(expected_output).resolve() == docx.resolve()
        except OSError:
            output_matches = False
    rows.append((
        "manifest_output_binding",
        "PASS" if output_matches else ("WARN" if allow_output_mismatch else "FAIL"),
        expected_output or "legacy manifest without a bound live output",
    ))

    source_info = manifest.get("source") or {}
    source_path = Path(source_info.get("path", "")) if source_info.get("path") else None
    source_state = "unavailable"
    source_ok = True
    if source_path and safe_is_file(source_path):
        source_ok = sha256_file(source_path) == source_info.get("sha256")
        source_state = "unchanged" if source_ok else "changed after preparation"
    rows.append(("source_snapshot", "PASS" if source_ok else "FAIL", source_state))

    intermediate_info = manifest.get("intermediate_docx") or {}
    intermediate_path = (
        Path(intermediate_info.get("path", "")) if intermediate_info.get("path") else None
    )
    intermediate_ok = bool(
        intermediate_path
        and safe_is_file(intermediate_path)
        and sha256_file(intermediate_path) == intermediate_info.get("sha256")
    )
    rows.append((
        "intermediate_binding",
        "PASS" if intermediate_ok else "FAIL",
        str(intermediate_path) if intermediate_path else "missing path",
    ))

    raw_ok = current["raw_citation_occurrences"] == 0
    rows.append((
        "raw_markers_removed", "PASS" if raw_ok else "FAIL",
        str(current["raw_citation_occurrences"]),
    ))
    live_ok = current["live_citation_fields"] == expected_clusters
    rows.append((
        "live_citation_fields",
        "PASS" if live_ok else ("INFO" if not require_live else "FAIL"),
        f"expected={expected_clusters}, actual={current['live_citation_fields']}",
    ))

    expected_items = expected_zotero_item_counts(manifest)
    actual_items = Counter(current.get("zotero_item_keys") or {})
    identity_available = expected_items is not None and current["live_citation_fields"] > 0
    identity_ok = bool(identity_available and expected_items == actual_items)
    if expected_items is None:
        identity_status = "INFO"
        identity_detail = "item identity unavailable for this citation-key source"
    else:
        identity_status = "PASS" if identity_ok else ("INFO" if not require_live else "FAIL")
        identity_detail = f"expected={dict(expected_items)}, actual={dict(actual_items)}"
    rows.append(("citation_item_identity", identity_status, identity_detail))

    unparsable = int(current.get("unparsable_citation_fields", 0))
    parse_ok = unparsable == 0
    rows.append((
        "citation_field_schema",
        "PASS" if parse_ok else ("INFO" if not require_live else "FAIL"),
        f"unparsable={unparsable}",
    ))

    preferences = current.get("zotero_preferences") or {}
    requested_style = normalize_style(job.get("style"))
    actual_style = normalize_style(preferences.get("style"))
    style_ok = not requested_style or requested_style == actual_style
    rows.append((
        "citation_style",
        "PASS" if style_ok else ("INFO" if not require_live else "FAIL"),
        f"requested={requested_style or 'unspecified'}, actual={actual_style or 'unavailable'}",
    ))
    requested_locale = normalize_locale(job.get("locale"))
    actual_locale = normalize_locale(preferences.get("locale"))
    locale_ok = not requested_locale or requested_locale == actual_locale
    rows.append((
        "citation_locale",
        "PASS" if locale_ok else ("INFO" if not require_live else "FAIL"),
        f"requested={requested_locale or 'unspecified'}, actual={actual_locale or 'unavailable'}",
    ))

    bibliography_ok = current["live_bibliography_fields"] == 1
    rows.append((
        "live_bibliography",
        "PASS" if bibliography_ok else ("INFO" if not require_bibliography else "FAIL"),
        f"expected={'1' if require_bibliography else 'optional'}, actual={current['live_bibliography_fields']}",
    ))
    structure_ok = not differences
    rows.append((
        "structure_preserved", "PASS" if structure_ok else "FAIL",
        "unchanged" if structure_ok else ", ".join(differences),
    ))

    required = [output_matches or allow_output_mismatch, source_ok, intermediate_ok, raw_ok, structure_ok]
    if require_live:
        required.extend([live_ok, parse_ok, style_ok, locale_ok])
        if expected_items is not None:
            required.append(identity_ok)
    if require_bibliography:
        required.append(bibliography_ok)
    status = "PASS" if all(required) else "FAIL"
    if status == "PASS":
        next_action = "complete"
    elif current["raw_citation_occurrences"] > 0 or current["live_citation_fields"] == 0:
        next_action = "run_odf_docx_scan"
    elif require_bibliography and not bibliography_ok:
        next_action = "open_word_refresh_and_bibliography"
    elif not style_ok or not locale_ok:
        next_action = "open_word_document_preferences_and_refresh"
    else:
        next_action = "inspect_failed_verification"
    return {
        "status": status,
        "checks": rows,
        "fingerprint": current,
        "next_action": next_action,
        "expected_clusters": expected_clusters,
    }


def safe_unlink(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        pass
    except OSError:
        # Temporary cleanup must never hide the conversion result or its error.
        pass


def run_deterministic_self_test(pandoc: Path) -> dict[str, Any]:
    token = uuid.uuid4().hex
    markdown = Path(tempfile.gettempdir()) / f"md-zotero-self-test-\u5f15\u7528-{token}.md"
    docx = Path(tempfile.gettempdir()) / f"md-zotero-self-test-{token}.docx"
    media = Path(tempfile.gettempdir()) / f"md-zotero-self-test-{token}.png"
    corrupt_docx = Path(tempfile.gettempdir()) / f"md-zotero-corrupt-{token}.docx"
    invalid_manifest = Path(tempfile.gettempdir()) / f"md-zotero-invalid-{token}.json"
    try:
        # A tiny valid PNG keeps this probe independent of user files and image apps.
        media.write_bytes(bytes.fromhex(
            "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
            "0000000d49444154789c6360f8cf00000004000101"
            "00000000ffff03000006000557bf"
            "0000000049454e44ae426082"
        ))
        markdown.write_text(
            "# Self Test\n\nA cluster [@codexSelfTest2026; @codex/testKey; @codex:test.key].\n\n"
            "Narrative @codexNarrative2026 and locator [@codexLocator2026, p. 12].\n\n"
            "A note.^[See @codexFootnote2026.]\n\n"
            "| A | B |\n|---|---|\n| [@codexTable2026] | 2 |\n\n"
            "![pixel](" + media.name + ")\n\n$$x = 1$$\n",
            encoding="utf-8",
        )
        stats = inspect_markdown(pandoc, markdown)
        media_findings = validate_media_targets(stats["image_targets"], [media.parent], False)
        run_pandoc(
            pandoc,
            ["--from=markdown+citations", "--to=docx", "--standalone", str(markdown), "--output", str(docx)],
            cwd=markdown.parent,
        )
        fingerprint = docx_fingerprint(docx, stats["citation_counts"])
        parsed_fields = zotero_field_summary([
            "ADDIN ZOTERO_ITEM CSL_CITATION "
            '{"citationItems":[{"uris":["http://zotero.org/users/local/test/items/AB12CD34"]}]}',
            'ADDIN ZOTERO_PREF_1 {"style":"http://www.zotero.org/styles/apa","locale":"en-US"}',
        ])
        known_component = {"state": "active", "version": "1.2.3", "path": "plugin.xpi"}
        unknown_component = {"state": "unknown"}
        partial_component = {
            "state": "available", "profile": None,
            "api": {"state": "running", "version": "10.0.1"},
        }
        prior_partial = {
            "state": "available", "profile": "profile/default",
            "api": {"state": "running", "version": "10.0.1"},
        }
        corrupt_docx.write_bytes(b"not-a-docx")
        try:
            docx_fingerprint(corrupt_docx)
            corrupt_guard = False
        except WorkflowError:
            corrupt_guard = True
        invalid_manifest.write_text("{", encoding="utf-8")
        try:
            load_manifest(invalid_manifest)
            manifest_guard = False
        except WorkflowError:
            manifest_guard = True
        probe_manifest = {
            "schema_version": SCHEMA_VERSION,
            "source": {"path": str(markdown), "sha256": sha256_file(markdown)},
            "intermediate_docx": {"path": str(docx), "sha256": sha256_file(docx)},
            "citations": stats,
            "key_validation": {"resolved_items": {}},
            "intermediate_fingerprint": fingerprint,
            "job": {
                "run_id": "self-test",
                "requested_mode": "delivery",
                "live_output": str(docx),
                "insert_bibliography": False,
                "current_stage": "prepared",
                "state": "prepared",
                "history": [],
            },
        }
        live_gate = evaluate_delivery_docx(docx, probe_manifest, require_live=True)
        checks = {
            "cluster_count": stats["citation_clusters"] == 5,
            "occurrence_count": stats["citation_occurrences"] == 7,
            "slash_key": stats["slash_keys"] == ["codex/testKey"],
            "dot_colon_key": "codex:test.key" in stats["citation_counts"],
            "narrative_locator_footnote_table": all(
                key in stats["citation_counts"]
                for key in (
                    "codexNarrative2026", "codexLocator2026",
                    "codexFootnote2026", "codexTable2026",
                )
            ),
            "raw_markers": fingerprint["raw_citation_occurrences"] == 7,
            "table": stats["tables"] == 1 and fingerprint["tables"] >= 1,
            "math": fingerprint["math_nodes"] >= 1,
            "media": len(media_findings) == 1 and media_findings[0]["state"] == "resolved",
            "missing_media_guard": resolve_media("definitely-missing-image.png", [media.parent])[1] == "missing",
            "unicode_path": "\u5f15\u7528" in markdown.name,
            "live_field_parser": (
                parsed_fields["live_citation_fields"] == 1
                and parsed_fields["zotero_item_keys"] == {"AB12CD34": 1}
                and parsed_fields["zotero_preferences"].get("locale") == "en-US"
            ),
            "unknown_component_uses_last_known_identity": (
                stabilized_component(unknown_component, known_component) == known_component
                and stabilized_component(partial_component, prior_partial).get("profile")
                == "profile/default"
            ),
            "default_live_gate": (
                live_gate["status"] == "FAIL"
                and live_gate["next_action"] == "run_odf_docx_scan"
            ),
            "corrupt_docx_guard": corrupt_guard,
            "invalid_manifest_guard": manifest_guard,
        }
        return {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}
    finally:
        safe_unlink(markdown)
        safe_unlink(docx)
        safe_unlink(media)
        safe_unlink(corrupt_docx)
        safe_unlink(invalid_manifest)


def compatibility_self_test(
    cache_dir: Path,
    capabilities: dict[str, Any],
    pandoc: Path,
    force: bool = False,
) -> dict[str, Any]:
    cache_path = cache_dir / "self-test-status.json"
    cached, cache_error = load_json(cache_path)
    fingerprint = capabilities.get("fingerprints", {}).get(
        "converter", capabilities["fingerprint"]
    )
    cache_matches = (
        not force
        and cached
        and cached.get("schema_version") == SCHEMA_VERSION
        and cached.get("tool_version") == TOOL_VERSION
        and cached.get("capability_fingerprint") == fingerprint
        and cached.get("status") == "PASS"
    )
    if cache_matches:
        return {**cached, "source": "cache", "cache_path": str(cache_path)}

    result = run_deterministic_self_test(pandoc)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "checked_at": now_iso(),
        "capability_fingerprint": fingerprint,
        "pandoc": capabilities["components"]["pandoc"],
        **result,
    }
    warnings = [cache_error] if cache_error else []
    try:
        atomic_json(cache_path, payload)
    except OSError as exc:
        warnings.append(f"Self-test cache was not written: {exc}")
    return {
        **payload,
        "source": "run",
        "cache_path": str(cache_path),
        **({"warnings": warnings} if warnings else {}),
    }


def cmd_doctor(args: argparse.Namespace) -> int:
    payload = doctor(Path(args.cache_dir).resolve())
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for name, component in payload["components"].items():
            print(f"{name}: {component.get('state', 'unknown')}")
        print(f"prepare_ready: {payload['ready']['prepare']}")
        print(f"delivery_ready: {payload['ready']['delivery']}")
    required = args.require
    return 0 if not required or payload["ready"][required] else 2


def cmd_refresh(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir).resolve()
    capabilities = doctor(cache_dir)
    keys, key_meta = refresh_key_index(
        cache_dir,
        force=True,
        capability_fingerprint=capabilities.get("fingerprints", {}).get(
            "citation_index", capabilities["fingerprint"]
        ),
    )
    payload = {"status": "PASS", "capabilities": capabilities, "key_index": key_meta, "unique_keys": len(keys)}
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"Refreshed {len(keys)} citation keys")
    return 0


def cmd_prepare(args: argparse.Namespace) -> int:
    source = Path(args.input).resolve()
    if not safe_is_file(source):
        raise WorkflowError(f"Markdown source not found: {source}")
    if source.suffix.lower() not in {".md", ".markdown"}:
        raise WorkflowError(f"Expected Markdown input, got: {source.suffix}")
    output = Path(args.output).resolve() if args.output else source.with_name(source.stem + "-intermediate.docx")
    manifest_path = Path(args.manifest).resolve() if args.manifest else output.with_suffix(".citation-manifest.json")
    report_path = Path(args.report).resolve() if args.report else output.with_suffix(".conversion-report.md")
    default_live_name = output.stem.removesuffix("-intermediate") + "-zotero-live.docx"
    live_output = (
        Path(args.live_output).resolve()
        if getattr(args, "live_output", None)
        else output.with_name(default_live_name)
    )
    unique_output(output, args.force)
    unique_output(manifest_path, args.force)
    unique_output(report_path, args.force)
    cache_dir = Path(args.cache_dir).resolve()
    capabilities = doctor(cache_dir)
    pandoc_sig = capabilities["components"]["pandoc"].get("signature")
    if not capabilities["ready"]["prepare"] or not pandoc_sig:
        raise WorkflowError("Pandoc is unavailable; run doctor and resolve the reported component")
    pandoc = Path(pandoc_sig["path"])
    compatibility = compatibility_self_test(cache_dir, capabilities, pandoc)
    if compatibility["status"] != "PASS":
        raise WorkflowError("Compatibility self-test failed; run self-test --json for the exact gate")
    roots = [source.parent]
    if args.vault_root:
        roots.append(Path(args.vault_root).resolve())
    roots.extend(Path(item).resolve() for item in args.resource_path)
    original = source.read_text(encoding="utf-8-sig")
    normalized, obsidian_findings = normalize_obsidian(original, list(dict.fromkeys(roots)))
    unresolved_embeds = [item for item in obsidian_findings if item["state"] != "resolved"]
    temp_md = Path(tempfile.gettempdir()) / f"md-zotero-{uuid.uuid4().hex}.md"
    temp_docx = output.with_name(f".{output.name}.{uuid.uuid4().hex}.tmp.docx")
    checks: list[tuple[str, str, str]] = []
    checks.append(("compatibility_self_test", "PASS", f"source={compatibility['source']}"))
    media_findings: list[dict[str, str]] = []
    try:
        temp_md.write_text(normalized, encoding="utf-8")
        stats = inspect_markdown(pandoc, temp_md)
        keys = list(stats["citation_counts"])
        key_source = "none"
        index: dict[str, list[dict[str, str]]] = {}
        key_meta: dict[str, Any] = {}
        key_fresh = True
        if keys:
            if args.bib_file:
                bibliography = Path(args.bib_file).resolve()
                if not safe_is_file(bibliography):
                    raise WorkflowError(f"BibTeX file not found: {bibliography}")
                try:
                    index = bibtex_index(bibliography)
                except OSError as exc:
                    raise WorkflowError(f"Cannot read BibTeX file {bibliography}: {exc}") from exc
                key_source = str(bibliography)
                key_meta = {"source": "bibtex", "path": str(bibliography), "key_count": len(index)}
            else:
                index, key_meta = refresh_key_index(
                    cache_dir,
                    capability_fingerprint=capabilities.get("fingerprints", {}).get(
                        "citation_index", capabilities["fingerprint"]
                    ),
                )
                key_source = key_meta["source"]
                key_fresh = key_meta.get("fresh", False)
                checks.append((
                    "key_index_freshness",
                    "PASS" if key_fresh else "WARN",
                    f"source={key_source}; fresh={key_fresh}",
                ))
        missing = sorted(key for key in keys if key not in index)
        ambiguous = {key: index[key] for key in keys if len(index.get(key, [])) > 1}
        if missing or ambiguous:
            detail = []
            if missing:
                detail.append("missing=" + ", ".join(missing))
            if ambiguous:
                detail.append("ambiguous=" + ", ".join(sorted(ambiguous)))
            checks.append(("citation_keys", "FAIL", "; ".join(detail)))
            if not args.allow_unverified_keys:
                raise WorkflowError("Citation-key validation failed: " + "; ".join(detail))
        else:
            checks.append(("citation_keys", "PASS", f"{len(keys)} unique keys via {key_source}"))
        if unresolved_embeds:
            detail = ", ".join(f"{item['target']} ({item['state']})" for item in unresolved_embeds)
            checks.append(("obsidian_media", "FAIL", detail))
            if not args.allow_missing_media:
                raise WorkflowError("Unresolved Obsidian embeds: " + detail)
        else:
            checks.append(("obsidian_media", "PASS", f"{len(obsidian_findings)} embeds resolved"))
        media_findings = validate_media_targets(
            stats["image_targets"], list(dict.fromkeys(roots)), args.allow_remote_media,
            args.allow_missing_media,
        )
        local_media = [item for item in media_findings if item["state"] == "resolved"]
        remote_media = [item for item in media_findings if item["state"] == "remote"]
        unresolved_media = [item for item in media_findings if item["state"] not in {"resolved", "remote"}]
        checks.append((
            "markdown_media",
            "PASS" if not unresolved_media else "FAIL",
            f"{len(local_media)} local resolved, {len(remote_media)} remote allowed, "
            f"{len(unresolved_media)} unresolved",
        ))
        pandoc_args = [
            "--from=markdown+citations", "--to=docx", "--standalone",
            str(temp_md), "--output", str(temp_docx),
            "--resource-path", os.pathsep.join(str(root) for root in roots),
        ]
        if args.reference_doc:
            reference_doc = Path(args.reference_doc).resolve()
            if not safe_is_file(reference_doc):
                raise WorkflowError(f"Reference DOCX not found: {reference_doc}")
            pandoc_args.extend(["--reference-doc", str(reference_doc)])
        run_pandoc(pandoc, pandoc_args, cwd=source.parent)
        os.replace(temp_docx, output)
        fingerprint = docx_fingerprint(output, keys)
        raw_expected = stats["citation_occurrences"]
        raw_actual = fingerprint["raw_citation_occurrences"]
        marker_ok = raw_actual == raw_expected
        checks.append(("raw_markers_preserved", "PASS" if marker_ok else "FAIL", f"expected={raw_expected}, actual={raw_actual}"))
        if not marker_ok:
            raise WorkflowError("Intermediate DOCX did not preserve every citation marker")
        resolved_items = {
            key: index[key][0]
            for key in keys
            if len(index.get(key, [])) == 1
        }
        blockers = delivery_blockers(capabilities) if args.mode == "delivery" else []
        if args.mode == "delivery" and not key_fresh:
            blockers.append("citation_key_index:fresh_required")
        delivery_fingerprint = capabilities.get("fingerprints", {}).get("delivery")
        canary = delivery_canary_status(cache_dir, delivery_fingerprint)
        if args.mode != "delivery":
            job_state = "prepared"
            waiting_for: list[str] = []
        elif not key_fresh:
            job_state = "waiting_for_delivery_components"
            waiting_for = ["citation_key_index:fresh_required"]
        else:
            job_state = "waiting_for_scan"
            waiting_for = ["odf_docx_scan"]
        created_at = now_iso()
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "tool_version": TOOL_VERSION,
            "created_at": created_at,
            "mode": args.mode,
            "source": {"path": str(source), "sha256": sha256_file(source)},
            "intermediate_docx": {"path": str(output), "sha256": sha256_file(output)},
            "pandoc": capabilities["components"]["pandoc"],
            "compatibility_self_test": compatibility,
            "citations": stats,
            "key_validation": {
                **key_meta, "missing": missing, "ambiguous": ambiguous,
                "verified": not missing and not ambiguous and key_fresh,
                "resolved_items": resolved_items,
            },
            "obsidian_embeds": obsidian_findings,
            "markdown_media": media_findings,
            "intermediate_fingerprint": fingerprint,
            "capability_fingerprint": capabilities["fingerprint"],
            "capability_fingerprints": capabilities.get("fingerprints", {}),
            "delivery_canary": canary,
            "job": {
                "run_id": "mdz-" + uuid.uuid4().hex,
                "requested_mode": args.mode,
                "style": args.style,
                "locale": args.locale,
                "insert_bibliography": bool(args.insert_bibliography),
                "live_output": str(live_output),
                "current_stage": job_state,
                "state": job_state,
                "waiting_for": waiting_for,
                "history": [{
                    "at": created_at,
                    "state": job_state,
                    "detail": "Intermediate DOCX prepared and verified",
                }],
            },
        }
        atomic_json(manifest_path, manifest)
        if any(row[1] == "FAIL" for row in checks):
            status = "DIAGNOSTIC_ONLY"
        elif any(row[1] == "WARN" for row in checks):
            status = "PASS_WITH_WARNINGS"
        else:
            status = "PASS"
        report = report_markdown(
            "Markdown To Zotero Word Preparation", status, checks,
            {
                "Source": source,
                "Intermediate DOCX": output,
                "Manifest": manifest_path,
                "Citation clusters": stats["citation_clusters"],
                "Citation occurrences": stats["citation_occurrences"],
                "Unique keys": stats["unique_citation_keys"],
                "Delivery state": job_state,
                "Live DOCX": live_output,
            },
        )
        atomic_write(report_path, report)
        payload = {
            "status": status, "output": str(output), "manifest": str(manifest_path),
            "report": str(report_path), "citations": stats,
            "key_validation": manifest["key_validation"], "checks": checks,
            "job_state": job_state, "waiting_for": waiting_for,
            "live_output": str(live_output), "delivery_canary": canary,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else report)
        return 0 if status in {"PASS", "PASS_WITH_WARNINGS"} else 2
    finally:
        safe_unlink(temp_md)
        safe_unlink(temp_docx)


def verify_report(
    docx: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    result: dict[str, Any],
    report_path: Path,
    force: bool,
) -> str:
    unique_output(report_path, force)
    report = report_markdown(
        "Zotero Live DOCX Verification", result["status"], result["checks"],
        {
            "DOCX": docx,
            "Manifest": manifest_path,
            "Run ID": manifest_job(manifest).get("run_id"),
            "SHA-256": sha256_file(docx),
            "Expected citation clusters": result["expected_clusters"],
            "Next action": result["next_action"],
        },
    )
    atomic_write(report_path, report)
    return report


def cmd_verify(args: argparse.Namespace) -> int:
    docx = Path(args.docx).resolve()
    manifest_path = Path(args.manifest).resolve()
    if not safe_is_file(docx) or not safe_is_file(manifest_path):
        raise WorkflowError("Both the live DOCX and preparation manifest must exist")
    manifest = load_manifest(manifest_path)
    require_live = not args.inspect_only
    result = evaluate_delivery_docx(
        docx,
        manifest,
        require_live=require_live,
        require_bibliography=args.require_bibliography,
        allow_output_mismatch=args.allow_output_mismatch,
    )
    report_path = Path(args.report).resolve() if args.report else docx.with_suffix(".conversion-report.md")
    report = verify_report(docx, manifest_path, manifest, result, report_path, args.force)
    payload = {
        **result,
        "docx": str(docx),
        "manifest": str(manifest_path),
        "report": str(report_path),
        "verification_mode": "inspect_only" if args.inspect_only else "live_required",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else report)
    return 0 if result["status"] == "PASS" else 2


def job_snapshot(
    manifest_path: Path,
    live_docx: Path | None,
    cache_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = load_manifest(manifest_path)
    job = manifest_job(manifest)
    binding_errors = manifest_binding_errors(manifest)
    if binding_errors:
        return manifest, {
            "status": "FAIL",
            "job_state": "failed",
            "next_action": "reprepare_changed_or_missing_artifact",
            "waiting_for": ["manual_inspection"],
            "manifest": str(manifest_path),
            "binding_errors": binding_errors,
        }
    requested_mode = job.get("requested_mode", manifest.get("mode", "delivery"))
    target = live_docx
    if target is None and job.get("live_output"):
        target = Path(job["live_output"]).resolve()
    if requested_mode != "delivery":
        return manifest, {
            "status": "PASS",
            "job_state": "prepared",
            "next_action": "complete_fast_mode",
            "manifest": str(manifest_path),
            "live_docx": str(target) if target else None,
        }

    capabilities = doctor(cache_dir)
    blockers = delivery_blockers(capabilities)
    delivery_fingerprint = capabilities.get("fingerprints", {}).get("delivery")
    canary = delivery_canary_status(cache_dir, delivery_fingerprint)
    verification: dict[str, Any] | None = None
    if target and safe_is_file(target):
        verification = evaluate_delivery_docx(
            target,
            manifest,
            require_live=True,
            require_bibliography=bool(job.get("insert_bibliography")),
        )
        if verification["status"] == "PASS":
            return manifest, {
                "status": "PASS",
                "job_state": "verified",
                "next_action": "complete",
                "manifest": str(manifest_path),
                "live_docx": str(target),
                "capabilities": capabilities,
                "delivery_canary": canary,
                "verification": verification,
            }

    # App discovery and optional canaries cannot block artifact-based handoff.
    if verification:
        next_action = verification["next_action"]
        if next_action.startswith("open_word"):
            state = "waiting_for_word_refresh"
            waiting_for = ["word_zotero_refresh"]
        elif next_action == "run_odf_docx_scan":
            state = "waiting_for_scan"
            waiting_for = ["odf_docx_scan"]
        else:
            state = "failed"
            waiting_for = ["manual_inspection"]
    else:
        state = "waiting_for_scan"
        next_action = "run_odf_docx_scan"
        waiting_for = ["odf_docx_scan"]
    return manifest, {
        "status": "WAITING" if state != "failed" else "FAIL",
        "job_state": state,
        "next_action": next_action,
        "waiting_for": waiting_for,
        "manifest": str(manifest_path),
        "intermediate_docx": (manifest.get("intermediate_docx") or {}).get("path"),
        "live_docx": str(target) if target else None,
        "capabilities": capabilities,
        "component_warnings": blockers,
        "delivery_canary": canary,
        **({"verification": verification} if verification else {}),
    }


def cmd_status(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).resolve()
    live_docx = Path(args.docx).resolve() if args.docx else None
    _, payload = job_snapshot(manifest_path, live_docx, Path(args.cache_dir).resolve())
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] != "FAIL" else 2


def cmd_resume(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).resolve()
    live_docx = Path(args.docx).resolve() if args.docx else None
    manifest, payload = job_snapshot(manifest_path, live_docx, Path(args.cache_dir).resolve())
    update_manifest_state(
        manifest_path,
        manifest,
        payload["job_state"],
        payload["next_action"],
        payload.get("waiting_for", []),
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] != "FAIL" else 2


def cmd_canary(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir).resolve()
    capabilities = doctor(cache_dir)
    delivery_fingerprint = capabilities.get("fingerprints", {}).get("delivery")
    cached = delivery_canary_status(cache_dir, delivery_fingerprint)
    if cached["status"] == "PASS" and not args.force:
        print(json.dumps({**cached, "source": "cache"}, ensure_ascii=False, indent=2))
        return 0

    pointer_path = cache_dir / "delivery-canary-current.json"
    pointer, _ = load_json(pointer_path)
    reuse = bool(
        not args.force
        and pointer
        and pointer.get("delivery_fingerprint") == delivery_fingerprint
        and safe_is_file(Path(pointer.get("manifest", "")))
    )
    if not reuse:
        index, key_meta = refresh_key_index(
            cache_dir,
            force=args.force,
            capability_fingerprint=capabilities.get("fingerprints", {}).get(
                "citation_index", capabilities["fingerprint"]
            ),
        )
        if not key_meta.get("fresh"):
            payload = {
                "status": "WAITING",
                "job_state": "waiting_for_delivery_components",
                "next_action": "refresh_citation_key_index",
                "waiting_for": ["citation_key_index:fresh_required"],
                "key_index": key_meta,
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
        citation_key = next((
            key for key in sorted(index, key=lambda value: (len(value), value.lower()))
            if len(index[key]) == 1
            and index[key][0].get("item_key")
            and index[key][0].get("title")
            and index[key][0].get("item_type") in CANARY_ITEM_TYPES
            and re.fullmatch(r"[A-Za-z0-9_./:+-]+", key)
        ), None)
        if not citation_key:
            raise WorkflowError("No unambiguous Zotero citation key is available for the delivery canary")
        token = (delivery_fingerprint or uuid.uuid4().hex)[:12] + "-" + uuid.uuid4().hex[:8]
        artifact_dir = cache_dir / "delivery-canary-artifacts"
        source = artifact_dir / f"canary-{token}.md"
        intermediate = artifact_dir / f"canary-{token}-intermediate.docx"
        manifest_path = artifact_dir / f"canary-{token}.json"
        report_path = artifact_dir / f"canary-{token}-prepare.md"
        live_docx = artifact_dir / f"canary-{token}-zotero-live.docx"
        atomic_write(
            source,
            "# Delivery Canary\n\nCompatibility probe [@" + citation_key + "].\n",
        )
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "prepare",
            str(source),
            "--output", str(intermediate),
            "--manifest", str(manifest_path),
            "--report", str(report_path),
            "--live-output", str(live_docx),
            "--mode", "delivery",
            "--cache-dir", str(cache_dir),
            "--json",
        ]
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if process.returncode != 0:
            raise WorkflowError(
                "Delivery canary preparation failed: " + (process.stderr.strip() or process.stdout.strip())
            )
        manifest = load_manifest(manifest_path)
        job = manifest_job(manifest)
        job["is_canary"] = True
        update_manifest_state(
            manifest_path,
            manifest,
            "waiting_for_scan",
            "run_odf_docx_scan",
            ["odf_docx_scan"],
        )
        pointer = {
            "schema_version": SCHEMA_VERSION,
            "tool_version": TOOL_VERSION,
            "created_at": now_iso(),
            "delivery_fingerprint": delivery_fingerprint,
            "citation_key": citation_key,
            "manifest": str(manifest_path),
            "intermediate_docx": str(intermediate),
            "live_docx": str(live_docx),
        }
        atomic_json(pointer_path, pointer)

    manifest_path = Path(pointer["manifest"]).resolve()
    live_docx = Path(pointer["live_docx"]).resolve()
    manifest, snapshot = job_snapshot(manifest_path, live_docx, cache_dir)
    update_manifest_state(
        manifest_path,
        manifest,
        snapshot["job_state"],
        snapshot["next_action"],
        snapshot.get("waiting_for", []),
    )
    if snapshot["job_state"] == "verified":
        status_path = cache_dir / "delivery-test-status.json"
        status_payload = {
            "schema_version": SCHEMA_VERSION,
            "tool_version": TOOL_VERSION,
            "checked_at": now_iso(),
            "status": "PASS",
            "delivery_fingerprint": delivery_fingerprint,
            "manifest": str(manifest_path),
            "live_docx": str(live_docx),
            "citation_key": pointer.get("citation_key"),
        }
        atomic_json(status_path, status_payload)
        snapshot["delivery_test_status"] = str(status_path)
    snapshot["canary"] = True
    snapshot["citation_key"] = pointer.get("citation_key")
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    return 0 if snapshot["status"] != "FAIL" else 2


def cmd_self_test(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir).resolve()
    capabilities = doctor(cache_dir)
    signature = capabilities["components"]["pandoc"].get("signature")
    if not signature:
        raise WorkflowError("Pandoc is unavailable")
    pandoc = Path(signature["path"])
    payload = compatibility_self_test(cache_dir, capabilities, pandoc, force=True)
    print(
        json.dumps(payload, ensure_ascii=False, indent=2)
        if args.json else "\n".join(f"{key}: {value}" for key, value in payload["checks"].items())
    )
    return 0 if payload["status"] == "PASS" else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=TOOL_VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    doctor_parser = sub.add_parser("doctor", help="Discover and cache current app/plugin capabilities")
    doctor_parser.add_argument("--cache-dir", default=str(default_cache_dir()))
    doctor_parser.add_argument("--require", choices=("prepare", "key_validation", "delivery"))
    doctor_parser.add_argument("--json", action="store_true")
    doctor_parser.set_defaults(func=cmd_doctor)

    refresh_parser = sub.add_parser("refresh", help="Refresh capabilities and the Zotero citation-key index")
    refresh_parser.add_argument("--cache-dir", default=str(default_cache_dir()))
    refresh_parser.add_argument("--json", action="store_true")
    refresh_parser.set_defaults(func=cmd_refresh)

    prepare_parser = sub.add_parser("prepare", help="Validate Markdown and create a marker-preserving DOCX")
    prepare_parser.add_argument("input")
    prepare_parser.add_argument("--output")
    prepare_parser.add_argument("--mode", choices=("fast", "delivery"), default="fast")
    prepare_parser.add_argument("--reference-doc")
    prepare_parser.add_argument("--bib-file", "--bibliography", dest="bib_file")
    prepare_parser.add_argument("--insert-bibliography", action="store_true")
    prepare_parser.add_argument("--style")
    prepare_parser.add_argument("--locale")
    prepare_parser.add_argument("--live-output")
    prepare_parser.add_argument("--vault-root")
    prepare_parser.add_argument("--resource-path", action="append", default=[])
    prepare_parser.add_argument("--cache-dir", default=str(default_cache_dir()))
    prepare_parser.add_argument("--manifest")
    prepare_parser.add_argument("--report")
    prepare_parser.add_argument("--allow-unverified-keys", action="store_true")
    prepare_parser.add_argument("--allow-missing-media", action="store_true")
    prepare_parser.add_argument("--allow-remote-media", action="store_true")
    prepare_parser.add_argument("--force", action="store_true")
    prepare_parser.add_argument("--json", action="store_true")
    prepare_parser.set_defaults(func=cmd_prepare)

    verify_parser = sub.add_parser("verify", help="Verify live Zotero fields and DOCX structure")
    verify_parser.add_argument("docx")
    verify_parser.add_argument("--manifest", required=True)
    verify_parser.add_argument("--require-live", action="store_true", help=argparse.SUPPRESS)
    verify_parser.add_argument(
        "--inspect-only", action="store_true",
        help="Inspect without requiring live Zotero citation fields",
    )
    verify_parser.add_argument("--require-bibliography", action="store_true")
    verify_parser.add_argument("--allow-output-mismatch", action="store_true")
    verify_parser.add_argument("--report")
    verify_parser.add_argument("--force", action="store_true")
    verify_parser.add_argument("--json", action="store_true")
    verify_parser.set_defaults(func=cmd_verify)

    status_parser = sub.add_parser("status", help="Inspect a resumable delivery job")
    status_parser.add_argument("manifest")
    status_parser.add_argument("--docx")
    status_parser.add_argument("--cache-dir", default=str(default_cache_dir()))
    status_parser.set_defaults(func=cmd_status)

    resume_parser = sub.add_parser("resume", help="Inspect and update a resumable delivery job")
    resume_parser.add_argument("manifest")
    resume_parser.add_argument("--docx")
    resume_parser.add_argument("--cache-dir", default=str(default_cache_dir()))
    resume_parser.set_defaults(func=cmd_resume)

    canary_parser = sub.add_parser(
        "canary", help="Prepare or verify a tiny live-citation compatibility job"
    )
    canary_parser.add_argument("--cache-dir", default=str(default_cache_dir()))
    canary_parser.add_argument("--force", action="store_true")
    canary_parser.set_defaults(func=cmd_canary)

    test_parser = sub.add_parser("self-test", help="Test deterministic conversion without user files")
    test_parser.add_argument("--cache-dir", default=str(default_cache_dir()))
    test_parser.add_argument("--json", action="store_true")
    test_parser.set_defaults(func=cmd_self_test)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except WorkflowError as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print(json.dumps({"status": "FAIL", "error": "Interrupted"}), file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
