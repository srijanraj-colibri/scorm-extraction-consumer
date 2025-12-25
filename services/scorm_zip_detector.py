import zipfile
import xml.etree.ElementTree as ET
from typing import List
from pydantic import BaseModel, Field


class ScormZipDetectionResult(BaseModel):
    is_scorm: bool
    is_valid: bool
    errors: List[str] = Field(default_factory=list)


class ScormZipDetector:
    MANIFEST = "imsmanifest.xml"

    def detect(self, zip_path: str) -> ScormZipDetectionResult:
        errors: List[str] = []

        if not zipfile.is_zipfile(zip_path):
            return ScormZipDetectionResult(
                is_scorm=False,
                is_valid=False,
                errors=["Not a ZIP file"],
            )

        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()

            manifest = next(
                (n for n in names if n.lower().endswith(self.MANIFEST)), None
            )
            if not manifest:
                return ScormZipDetectionResult(
                    is_scorm=False,
                    is_valid=False,
                    errors=["imsmanifest.xml not found"],
                )

            data = zf.read(manifest)
            if not data.strip():
                errors.append("imsmanifest.xml is empty")

            try:
                root = ET.fromstring(data)
            except ET.ParseError as e:
                return ScormZipDetectionResult(
                    is_scorm=True,
                    is_valid=False,
                    errors=[f"Malformed XML: {e}"],
                )

            ns = self._ns(root)
            if root.find(f"{ns}resources") is None:
                errors.append("<resources> missing")
            if root.find(f"{ns}organizations") is None:
                errors.append("<organizations> missing")

        return ScormZipDetectionResult(
            is_scorm=True,
            is_valid=len(errors) == 0,
            errors=errors,
        )

    def _ns(self, root):
        return root.tag.split("}")[0] + "}" if root.tag.startswith("{") else ""
