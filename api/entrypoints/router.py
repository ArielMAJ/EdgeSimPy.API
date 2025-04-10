# from api.entrypoints import auth, user
from api.entrypoints import background_test
from fastapi.routing import APIRouter

# user.router.include_router(user.authenticated_router)

router = APIRouter()
# router.include_router(user.router, prefix="/user", tags=["User"])
# router.include_router(auth.router, prefix="/auth", tags=["Auth"])

router.include_router(
    background_test.router, prefix="/background_test", tags=["Background Test"]
)
