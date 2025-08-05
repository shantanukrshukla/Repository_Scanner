import logging
from pathlib import Path

# Ensure the directory exists before setting up logging
log_dir = Path("app_activity")
log_dir.mkdir(parents=True, exist_ok=True)

# Now configure logging
logging.basicConfig(
    filename=log_dir / "agent_activity.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)
