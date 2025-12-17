import json
import logging
import stomp
from consumer.schema import AlfrescoEvent
from settings import settings
from workers.tasks import auto_tag_node

logger = logging.getLogger("consumer")


class UploadEventListener(stomp.ConnectionListener):

    def __init__(self, conn):
        self.conn = conn

    def on_message(self, frame):
        ack_id = frame.headers["ack"]
        sub_id = frame.headers["subscription"]

        try:
            payload = json.loads(frame.body)
            event = AlfrescoEvent(**payload)

            if event.eventType != "CONTENT_READY":
                self._ack(ack_id, sub_id)
                return

            result = auto_tag_node.apply_async(
                args=[payload]
            ).get(timeout=settings.WORKER_TIMEOUT)

            if result is True:
                self._ack(ack_id, sub_id)
                logger.info(f"ACKed {ack_id}")
            else:
                raise RuntimeError("Worker failed")

        except Exception:
            logger.exception("Processing failed – NO ACK")

    def _ack(self, ack_id, sub_id):
        self.conn.send_frame(
            "ACK",
            headers={"id": ack_id, "subscription": sub_id}
        )
