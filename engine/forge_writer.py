# /CppForge/engine/forge_writer.py
# CppForge File Writer (multi-file C++ support)
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



# system imports
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple



# ===========================================
# FORGE WRITER CLASS
# ===========================================
class ForgeWriter:
    """
    ForgeWriter
    - Writes C++ files into storage/pending
    - Supports multi-file output (.hpp/.h/.hh/.hxx + .cpp)
    - Saves arbitrary files into storage/saved
    - Logs actions into storage/logs/forge.log
    """

    # --------------
    # Initialize
    # --------------
    def __init__(self, storage_root: Path):
        self.storage_root = Path(storage_root)
        self.pending_dir = self.storage_root / "pending"
        self.saved_dir = self.storage_root / "saved"
        self.logs_dir = self.storage_root / "logs"
        self.log_path = self.logs_dir / "forge.log"

        self.pending_dir.mkdir(parents=True, exist_ok=True)
        self.saved_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # Inject Brand Tag
    # -------------------------
    def _inject_brand_tag(self, code: str) -> str:
        """
        Injects GlyphicMind Solutions Brand into C++ file.
        """
        lines = code.splitlines()
        brand = "//--- Created with GlyphicMind Solutions: CppForge ---//"

        if len(lines) >= 3:
            lines.insert(2, brand)
        else:
            while len(lines) < 2:
                lines.append("")
            lines.append(brand)

        return "\n".join(lines)

    # -------------------------
    # Detect multi-file output
    # -------------------------
    def _split_cpp_files(self, raw: str) -> Dict[str, str]:
        """
        Detects and splits multi-file C++ output.

        Expected patterns:
            // FILE: MyClass.hpp
            // FILE: MyClass.cpp

        Returns:
            { "MyClass.hpp": "<code>", "MyClass.cpp": "<code>" }
        """
        files: Dict[str, str] = {}
        current_name = None
        current_lines: List[str] = []

        for line in raw.splitlines():
            if line.strip().startswith("// FILE:"):
                # save previous file if exists
                if current_name and current_lines:
                    files[current_name] = "\n".join(current_lines).strip()

                # start new file
                current_name = line.split(":", 1)[1].strip()
                current_lines = []
            else:
                if current_name:
                    current_lines.append(line)

        # save last file
        if current_name and current_lines:
            files[current_name] = "\n".join(current_lines).strip()

        return files

    # -------------------------
    # Forge script(s)
    # -------------------------
    def forge_script(self, filename: str, code: str, purpose: str = "") -> bool:
        """
        Forges C++ file(s) and writes them to storage/pending.
        Supports multi-file output.
        """
        # Detect multi-file output
        file_map = self._split_cpp_files(code)

        # If no multi-file markers, treat as single file
        if not file_map:
            if not (filename.endswith(".cpp") or filename.endswith(".hpp") or filename.endswith(".h")):
                filename += ".cpp"

            path = self.pending_dir / filename
            code = self._inject_brand_tag(code)

            try:
                path.write_text(code, encoding="utf-8")
            except Exception as e:
                print(f"⚠️ Failed to write C++ file: {e}")
                return False

            self._log_event("forge_pending", {
                "filename": filename,
                "purpose": purpose,
                "path": str(path)
            })

            print(f"🛠️ C++ file forged (pending): {path}")
            return True

        # Multi-file output
        success = True
        for fname, fcode in file_map.items():
            fcode = self._inject_brand_tag(fcode)
            path = self.pending_dir / fname

            try:
                path.write_text(fcode, encoding="utf-8")
            except Exception as e:
                print(f"⚠️ Failed to write C++ file '{fname}': {e}")
                success = False
                continue

            self._log_event("forge_pending", {
                "filename": fname,
                "purpose": purpose,
                "path": str(path)
            })

            print(f"🛠️ C++ file forged (pending): {path}")

        return success

    # -------------------------
    # Save script(s)
    # -------------------------
    def save_script(self, filename: str, code: str) -> bool:
        """
        Saves C++ file(s) directly to storage/saved.
        Supports multi-file output.
        """
        file_map = self._split_cpp_files(code)

        # Single file
        if not file_map:
            if not (filename.endswith(".cpp") or filename.endswith(".hpp") or filename.endswith(".h")):
                filename += ".cpp"

            path = self.saved_dir / filename
            code = self._inject_brand_tag(code)

            try:
                path.write_text(code, encoding="utf-8")
            except Exception as e:
                print(f"⚠️ Failed to save C++ file: {e}")
                return False

            self._log_event("save_script", {
                "filename": filename,
                "path": str(path)
            })

            print(f"💾 C++ file saved: {path}")
            return True

        # Multi-file
        success = True
        for fname, fcode in file_map.items():
            fcode = self._inject_brand_tag(fcode)
            path = self.saved_dir / fname

            try:
                path.write_text(fcode, encoding="utf-8")
            except Exception as e:
                print(f"⚠️ Failed to save C++ file '{fname}': {e}")
                success = False
                continue

            self._log_event("save_script", {
                "filename": fname,
                "path": str(path)
            })

            print(f"💾 C++ file saved: {path}")

        return success

    # -------------------------
    # Log event
    # -------------------------
    def _log_event(self, event_type: str, details: dict):
        """
        Logs the event to storage/logs/forge.log
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "details": details,
        }

        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"⚠️ Failed to write forge log: {e}")

