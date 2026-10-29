"""
System & Environment Configuration Schemas.
"""

from pydantic import BaseModel, Field


class SystemConfigResponse(BaseModel):
    """
    Safe, masked view of currently active environment configuration.
    Secrets and passwords are deliberately masked.
    """
    environment: str = Field(..., description="Active environment name (dev/prod)")
    env_file_source: str = Field(..., description="Path to active source .env file")
    app_name: str = Field(..., description="Registered app name")
    version: str = Field(..., description="Service version")
    debug: bool = Field(..., description="Debug mode")
    log_level: str = Field(..., description="Logging verbosity")
    host: str = Field(..., description="Bound host")
    port: int = Field(..., description="Bound port")
    cors_origins: list[str] = Field(..., description="Allowed origins")
    database_url_masked: str = Field(..., description="Masked database URI")
    redis_url_masked: str = Field(..., description="Masked Redis URI")



class EnvSwitchRequest(BaseModel):
    environment: str = Field(..., description="Target environment: 'dev' or 'prod'")


class EnvSwitchResponse(BaseModel):
    previous_environment: str
    active_environment: str
    active_env_file: str
    message: str
