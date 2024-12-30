import uuid

def is_valid_uuid(value):
    try:
        # Attempt to create a UUID object from the value
        uuid_obj = uuid.UUID(str(value))
        return True
    except ValueError:
        # ValueError is raised if the value is not a valid UUID
        return False