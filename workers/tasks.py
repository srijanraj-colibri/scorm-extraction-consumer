import os
import tempfile
import requests
from celery import shared_task

from core.schema import RepoEvent
from core.settings import settings

from services.alfresco_client import AlfrescoClient
from services.scorm_zip_detector import ScormZipDetector
from services.scorm_extractor import ScormExtractor
from services.scorm_uploader import ScormUploader
from services.exceptions import ScormValidationError


def _extract_node_id(node_ref: str) -> str:
    """
    workspace://SpacesStore/<uuid> → <uuid>
    """
    if not node_ref or "/" not in node_ref:
        raise ValueError(f"Invalid nodeRef: {node_ref}")
    return node_ref.split("/")[-1]


@shared_task(
    bind=True,
    autoretry_for=(requests.HTTPError, RuntimeError),
    retry_kwargs={"max_retries": 5, "countdown": 15},
)
def process_scorm_zip(self, payload: dict) -> bool:
    """
    End-to-end SCORM ZIP processing based on RepoEvent payload.

    Flow:
    - Validate payload schema
    - Download ZIP from Alfresco
    - Validate SCORM (imsmanifest.xml sanity)
    - Create folder (same parent, ZIP name)
    - Extract safely
    - Upload extracted content
    """

    event = RepoEvent.model_validate(payload)

    if event.eventType != "BINARY_CHANGED":
        return True

    if not event.name or not event.name.lower().endswith(".zip"):
        return True

    if event.mimeType and event.mimeType != "application/zip":
        return True

    if not event.nodeRef or not event.parentNodeRef:
        raise RuntimeError("Missing nodeRef or parentNodeRef")

    zip_node_id = _extract_node_id(event.nodeRef)
    parent_node_id = _extract_node_id(event.parentNodeRef)

    zip_name = event.name
    target_folder_name = os.path.splitext(zip_name)[0]

    client = AlfrescoClient(
        settings.ALFRESCO_BASE_URL,
        settings.ALFRESCO_USERNAME,
        settings.ALFRESCO_PASSWORD,
    )

    detector = ScormZipDetector()
    extractor = ScormExtractor()
    uploader = ScormUploader(client)

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = os.path.join(tmp, zip_name)
        extract_dir = os.path.join(tmp, "extracted")

        try:
            client.download_content(zip_node_id, zip_path)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                raise RuntimeError(
                    f"Binary not yet available for node {zip_node_id}"
                )
            raise

        result = detector.detect(zip_path)
        if not result.is_scorm or not result.is_valid:
            raise ScormValidationError(result.errors)

        target_folder_id = client.create_folder(
            name=target_folder_name,
            parent_id=parent_node_id,
        )

        extractor.extract(zip_path, extract_dir)

        uploader.upload_directory(extract_dir, target_folder_id)

    return True
