
import logging
from typing import Optional

from fastapi import Request

class TraceIDFilter():

    def __init__(self, trace_id: Optional[str] = None):
        self.trace_id = trace_id or "N/A"

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = getattr(record, "trace_id", self.trace_id)
        return True
    