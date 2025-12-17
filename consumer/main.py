import time
import signal
import stomp
import logging

from settings import settings
from consumer.stomp_listener import UploadEventListener

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

shutdown = False


def stop(*_):
    global shutdown
    shutdown = True
    logger.info("Shutdown signal received")


signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)

conn = stomp.Connection12(
    [(settings.ACTIVEMQ_HOST, settings.ACTIVEMQ_PORT)],
    heartbeats=(
        settings.ACTIVEMQ_HEARTBEAT_OUT,
        settings.ACTIVEMQ_HEARTBEAT_IN,
    ),
)

conn.set_listener("", UploadEventListener(conn))

conn.connect(
    settings.ACTIVEMQ_USER,
    settings.ACTIVEMQ_PASSWORD,
    wait=True,
)

conn.subscribe(
    destination=settings.ACTIVEMQ_QUEUE,
    id="upload-consumer",
    ack="client-individual",
    headers={
        "activemq.prefetchSize": str(settings.ACTIVEMQ_PREFETCH)
    },
)

logger.info("Upload consumer started and listening...")

while not shutdown:
    time.sleep(1)

logger.info("Disconnecting from ActiveMQ")
conn.disconnect()
