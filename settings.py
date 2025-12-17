from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ---------- ActiveMQ (consumer only) ----------
    ACTIVEMQ_HOST: str | None = None
    ACTIVEMQ_PORT: int = 61613
    ACTIVEMQ_USER: str | None = None
    ACTIVEMQ_PASSWORD: str | None = None
    ACTIVEMQ_QUEUE: str | None = None

    ACTIVEMQ_PREFETCH: int = 1
    ACTIVEMQ_HEARTBEAT_OUT: int = 10000
    ACTIVEMQ_HEARTBEAT_IN: int = 10000

    # ---------- Redis ----------
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    # ---------- Celery ----------
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # ---------- Worker ----------
    WORKER_TIMEOUT: int = 600

    class Config:
        extra = "ignore"


settings = Settings()
