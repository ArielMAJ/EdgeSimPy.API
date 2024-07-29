# from api.entrypoints import auth, user
from fastapi.routing import APIRouter

# user.router.include_router(user.authenticated_router)

router = APIRouter()
# router.include_router(user.router, prefix="/user", tags=["User"])
# router.include_router(auth.router, prefix="/auth", tags=["Auth"])
