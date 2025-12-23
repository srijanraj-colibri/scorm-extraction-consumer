import json
import logging
import stomp

from core.schema import RepoEvent
from core.settings import settings
from workers.tasks import auto_tag_node

logger = logging.getLogger(__name__)


class UploadEventListener(stomp.ConnectionListener):

    def __init__(self, conn):
        self.conn = conn

    def on_message(self, frame):
        ack_id = frame.headers["ack"]
        sub_id = frame.headers["subscription"]

        try:
            payload = json.loads(frame.body)

            # ✅ Canonical schema validation
            event = RepoEvent.model_validate(payload)

            if event.eventType != "BINARY_CHANGED":
                self._ack(ack_id, sub_id)
                return

            result = auto_tag_node.apply_async(
                args=[payload]
            ).get(timeout=settings.WORKER_TIMEOUT)

            if result is True:
                self._ack(ack_id, sub_id)
                logger.info("ACKed %s", ack_id)
            else:
                raise RuntimeError("Worker failed")

        except Exception:
            logger.exception("Processing failed – NO ACK")

    def _ack(self, ack_id, sub_id):
        self.conn.send_frame(
            "ACK",
            headers={"id": ack_id, "subscription": sub_id},
        )
