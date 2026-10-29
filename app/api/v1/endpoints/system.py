"""
System Diagnostics & Dynamic Environment Switcher Endpoint.
"""

from fastapi import APIRouter, status
from app.api.deps import SettingsDep
from app.core.config import reload_settings
from app.core.environment import (
    EnvironmentType,
    get_active_environment,
    get_env_file_path,
    set_active_environment,
)
from app.core.security import mask_sensitive_value
from app.schemas.base import StandardResponse
from app.schemas.system import (
    EnvSwitchRequest,
    EnvSwitchResponse,
    SystemConfigResponse,
)

router = APIRouter(prefix="/system", tags=["System & Environment"])



@router.get(
    "/config",
    response_model=StandardResponse[SystemConfigResponse],
    status_code=status.HTTP_200_OK,
    summary="Inspect Active Environment Configuration",
    description="Returns current configuration variables loaded from either .env.dev or .env.prod with secrets masked.",
)
async def get_system_configuration(settings: SettingsDep) -> StandardResponse[SystemConfigResponse]:
    active_env = get_active_environment()
    source_file = str(get_env_file_path(active_env))

    data = SystemConfigResponse(
        environment=settings.APP_ENV,
        env_file_source=source_file,
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        log_level=settings.LOG_LEVEL,
        host=settings.HOST,
        port=settings.PORT,
        cors_origins=settings.CORS_ORIGINS,
        database_url_masked=mask_sensitive_value(settings.DATABASE_URL, 12),
        redis_url_masked=mask_sensitive_value(settings.REDIS_URL, 6),
    )
    return StandardResponse(success=True, data=data)


@router.post(
    "/env-switch",
    response_model=StandardResponse[EnvSwitchResponse],
    status_code=status.HTTP_200_OK,
    summary="Runtime Environment Swapper",
    description="Swap active variables between .env.dev and .env.prod at runtime without restarting the container.",
)
async def swap_environment_runtime(payload: EnvSwitchRequest) -> StandardResponse[EnvSwitchResponse]:
    previous_env = get_active_environment().value
    match payload.environment.strip().lower():
        case "prod" | "production":
            target_env = EnvironmentType.PROD
        case _:
            target_env = EnvironmentType.DEV

    # Swap active environment in memory and reload settings from disk
    set_active_environment(target_env)
    new_settings = reload_settings()
    active_file = str(get_env_file_path(target_env))

    data = EnvSwitchResponse(
        previous_environment=previous_env,
        active_environment=new_settings.APP_ENV,
        active_env_file=active_file,
        message=f"Successfully swapped runtime variables to {new_settings.APP_ENV.upper()} (loaded from {active_file}).",
    )
    return StandardResponse(success=True, data=data)
