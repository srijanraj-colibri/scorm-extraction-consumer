import time
import signal
import stomp
import logging

from core.settings import settings
from core.logging_config import setup_logging
from consumer.listener import UploadEventListener   

shutdown = False
logger = logging.getLogger(__name__)


def stop(*_):
    global shutdown
    shutdown = True
    logger.info("Shutdown signal received")


def main():
    setup_logging(settings.LOG_LEVEL)

    logger.info("Starting upload event consumer")

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    conn = stomp.Connection12(
        [(settings.ACTIVEMQ_HOST, settings.ACTIVEMQ_PORT)],
        heartbeats=(
            settings.ACTIVEMQ_HEARTBEAT_OUT,
            settings.ACTIVEMQ_HEARTBEAT_IN,
        ),
    )

    conn.set_listener(
        "upload-consumer",
        UploadEventListener(conn),
    )

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

    logger.info("Upload consumer started")

    while not shutdown:
        time.sleep(1)

    logger.info("Disconnecting from ActiveMQ")
    conn.disconnect()


if __name__ == "__main__":
    main()
