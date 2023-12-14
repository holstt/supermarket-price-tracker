import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class DataStorage:
    def __init__(self, base_dir: Path, store_name: str):
        self.data_dir = self._create_data_directory(base_dir, store_name)

    def save_data(
        self,
        file_name: str,
        data: dict[Any, Any],
    ):
        save_path = self.data_dir / file_name
        with open(save_path, "w") as f:
            json.dump(data, f)
        logger.debug(f"Saved data to: {save_path}")

    def _create_data_directory(self, base_dir: Path, store_name: str):
        data_dir = Path(
            base_dir, store_name, datetime.utcnow().strftime("%Y-%m-%d__%H-%M-%S")
        )
        data_dir.mkdir(parents=True, exist_ok=False)
        logger.info(f"Created data directory: {data_dir}")
        return data_dir
