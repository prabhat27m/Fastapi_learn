from fastapi import APIRouter
from .. import schemas

router= APIRouter(
    tags=['auth']
)

@router.post('/login')
def login(request: schemas.Login):
    return 'login'
