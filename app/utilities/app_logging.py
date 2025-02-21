import logging.config
import yaml
import os

def configure_logging():
    """Load YAML-based logging configuration."""
    yaml_path = os.path.abspath("log_config.yaml")

    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config)

class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.ERROR, logging.CRITICAL)
    