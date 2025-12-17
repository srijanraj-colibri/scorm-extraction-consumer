from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    host: str = Field(
        default="localhost",
        description="ActiveMQ host or service name"
    )
    port: int = Field(
        default=61613,
        ge=1,
        le=65535,
        description="STOMP port"
    )
    user: str = Field(default="admin")
    password: str = Field(default="admin")

    queue_name: str = Field(
        default="/queue/alfresco.upload.events",
        description="STOMP destination"
    )

    heartbeat_out: int = Field(default=10000, ge=0)
    heartbeat_in: int = Field(default=10000, ge=0)

    prefetch: int = Field(default=1, ge=1)

    model_config = {
        "env_prefix": "ACTIVEMQ_",
        "env_file": ".env",
        "extra": "ignore",
    }

