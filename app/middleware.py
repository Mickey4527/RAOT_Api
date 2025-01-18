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

# from fastapi import Request, HTTPException, status
# from fastapi.responses import JSONResponse
# from app.services.token_service import TokenService
# from app.config import settings


# async def add_jwt_to_response(request: Request, call_next):
#     response = await call_next(request)

#     # Check if the response is successful (status code 200)
#     if response.status_code == 200:
#         # Read the body of the response
#         body = b"".join([chunk async for chunk in response.body_iterator])
#         response_data = body.decode("utf-8")

#         # Create JWT
#         jwt_token = TokenService().create_jwt_token({"response_data": response_data})

#         # Return a new JSON response with the JWT
#         return JSONResponse(content=jwt_token)

#     return response

# async def validate_host(request: Request, call_next):
#     allowed_host = settings.FRONTEND_HOST
#     origin = request.headers.get("origin")

#     if origin != allowed_host:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

#     return await call_next(request)