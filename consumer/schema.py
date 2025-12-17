from pydantic import BaseModel
from typing import Literal


class AlfrescoEvent(BaseModel):
    nodeRef: str
    eventType: Literal[
        "NODE_CREATED",
        "CONTENT_READY",
        "METADATA_CHANGED",
        "AUDIT_UPDATED",
        "NODE_DELETED",
    ]
