# from fastapi import HTTPException
# from fastapi import Request
# from fastapi.middleware.base import BaseHTTPMiddleware
# EXLUDED_PATHS = ['docs', 'openapi.json']

# def translate_method_to_action(method: str) -> str:
#     method_permission_mapping = {
#         'GET': 'read',
#         'POST': 'write',
#         'PUT': 'update',
#         'DELETE': 'delete',
#     }
#     return method_permission_mapping.get(method.upper(), 'read')


# def has_permission(user_role, resource_name, required_permission):
#     if user_role in RESOURCES_FOR_ROLES and resource_name in RESOURCES_FOR_ROLES[user_role]:
#         return required_permission in RESOURCES_FOR_ROLES[user_role][resource_name]
#     return False

# # Define a custom Middleware for handling RBAC
# class RBACMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         request_method = str(request.method).upper()
#         action = translate_method_to_action(request_method)
#         resource = request.url.path[1:]
#         if not resource in EXLUDED_PATHS:
#             admin1 = USERS['admin1']  # Switch between user and admin by commenting out this or the next line
#             # user1 = USERS['user1']
#             if not has_permission(admin1['role'], resource, action):
#                 raise HTTPException(status_code=403, detail="Insufficient permissions")
#         response = await call_next(request)
#         return response