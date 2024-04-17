from fastapi import APIRouter, status
from controllers import Controllers
from typing import List

router = APIRouter()


router.get(
        "/",
        status_code=status.HTTP_200_OK
        )(Controllers.root)


router.get(
        "/bdays/",
        status_code=status.HTTP_200_OK,
        )(Controllers.list_birthdays)


router.post(
        "/bday/new",
        status_code=status.HTTP_201_CREATED
        )(Controllers.add_birthday)
