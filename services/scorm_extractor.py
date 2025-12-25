import zipfile
import os
from services.exceptions import UnsafeZipError


class ScormExtractor:
    def extract(self, zip_path: str, target_dir: str):
        with zipfile.ZipFile(zip_path) as zf:
            for m in zf.infolist():
                self._safe_extract(zf, m, target_dir)

    def _safe_extract(self, zf, member, target_dir):
        normalized = os.path.normpath(member.filename)

        if normalized.startswith("..") or os.path.isabs(normalized):
            raise UnsafeZipError(f"Unsafe ZIP entry: {member.filename}")

        dest = os.path.join(target_dir, normalized)
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        with zf.open(member) as src, open(dest, "wb") as dst:
            dst.write(src.read())
