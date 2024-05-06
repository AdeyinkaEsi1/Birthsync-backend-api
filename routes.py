from fastapi import APIRouter, status
from controllers import Controllers


router = APIRouter()


router.get(
        "/bdays/",
        tags=["Birthdays"],
        status_code=status.HTTP_200_OK
        )(Controllers.list_birthdays)


router.post(
        "/bday/new",
        tags=["Birthdays"],
        status_code=status.HTTP_201_CREATED
        )(Controllers.add_birthday)


router.put(
        "/bday/update",
        tags=["Birthdays"],
        status_code=status.HTTP_202_ACCEPTED
        )(Controllers.update_birthday)


router.get(
        "/bday/get",
        tags=["Birthdays"],
        status_code=status.HTTP_200_OK
        )(Controllers.get_birthday)


router.delete(
        "/bday/get",
        tags=["Birthdays"],
        status_code=status.HTTP_204_NO_CONTENT
        )(Controllers.delete_birthday)


router.post(
        "/auth/register",
        tags=["Auth"],
        status_code=status.HTTP_201_CREATED
        )(Controllers.sign_up)


router.post(
        "/auth/sign_in",
        tags=["Auth"],
        status_code=status.HTTP_200_OK,
        )(Controllers.sign_in)


router.get(
    "/auth/users",
    tags=["Users"],
    status_code=status.HTTP_200_OK,
    )(Controllers.list_users)

