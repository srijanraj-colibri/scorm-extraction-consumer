from workers.celery_app import celery_app
from workers.idempotency import already_processed, mark_processed
import time
import logging

logger = logging.getLogger(__name__)


@celery_app.task
def auto_tag_node(payload: dict) -> bool:
    node_ref = payload["nodeRef"]
    event_type = payload["eventType"]
    key = f"{node_ref}:{event_type}"

    if already_processed(key):
        logger.info(f"Skipping duplicate {key}")
        return True

    logger.info(f"Processing {node_ref}")
    time.sleep(30)  # simulate AI work

    mark_processed(key)
    logger.info(f"Completed {node_ref}")
    return True
