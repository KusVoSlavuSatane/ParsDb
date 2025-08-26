from pathlib import Path

from loguru import logger

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

log_file = log_dir / "app.log"

logger.remove()
logger.add(
    log_file,
    rotation="10 MB",  # ротация при достижении 10МБ
    retention="10 days",  # хранить логи 10 дней
    compression="zip",  # старые логи сжимать
    level="DEBUG",  # писать всё
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "{message}",
)

__all__ = ["logger"]
