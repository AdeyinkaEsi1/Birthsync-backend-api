from fastapi import APIRouter, status
from controllers import Controllers
from schemas import PersonResponseSchema
from typing import List

router = APIRouter()


router.get("/",
           status_code=status.HTTP_200_OK
           )(Controllers.root)


router.get("/bdays/",
           status_code=status.HTTP_200_OK,
           )(Controllers.list_birthdays)