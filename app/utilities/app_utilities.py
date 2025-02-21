import uuid

def generate_trace_id() -> str:
    """
    Generate a unique trace ID.
    """
    return str(uuid.uuid4()) 