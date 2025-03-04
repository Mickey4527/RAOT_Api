import os
import casbin
import casbin_async_sqlalchemy_adapter
from app.core.config import settings

async def get_casbin_enforcer() -> casbin.AsyncEnforcer:
    """
    Initialize Casbin AsyncEnforcer with the SQLAlchemy adapter
    """

    adapter = casbin_async_sqlalchemy_adapter.Adapter(str(settings.SQLALCHEMY_DATABASE_URI))
    path_enforcer = os.path.join(os.path.dirname(__file__), 'rbac_model.conf')
    
    enforcer = casbin.AsyncEnforcer(path_enforcer, adapter)
    await enforcer.load_policy()

    return enforcer