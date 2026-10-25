"""
Enterprise CLI Server Runner.
==============================================================================
Allows starting the FastAPI backend with explicit environment flags:
    python run.py              # Uses environment set in app/core/environment.py
    python run.py --env dev    # Forces development environment (.env.dev)
    python run.py --env prod   # Forces production environment (.env.prod)
==============================================================================
"""

import argparse
import sys
import uvicorn

from app.core.config import reload_settings
from app.core.environment import (
    EnvironmentType,
    get_active_environment,
    get_env_file_path,
    set_active_environment,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Enterprise Multi-Agent Business Operations Backend."
    )
    parser.add_argument(
        "--env",
        choices=["dev", "prod"],
        default=None,
        help="Target environment (overrides app/core/environment.py)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="Host interface to bind (defaults to config)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to listen on (defaults to config)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        default=None,
        help="Force enable auto-reload",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    # Apply environment override if provided via CLI flag
    if args.env:
        target_env = EnvironmentType(args.env)
        set_active_environment(target_env)

    # Load validated settings from target environment file
    settings = reload_settings()
    active_env = get_active_environment()
    env_file = get_env_file_path(active_env)

    host = args.host or settings.HOST
    port = args.port or settings.PORT
    reload = args.reload if args.reload is not None else settings.RELOAD

    print(f"\n[CLI] Starting {settings.APP_NAME}")
    print(f"[CLI] Environment: {active_env.value.upper()} (Source: {env_file})")
    print(f"[CLI] Listening on: http://{host}:{port} (Reload: {reload})\n")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()
