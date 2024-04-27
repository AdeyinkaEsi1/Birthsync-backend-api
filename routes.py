
from fastapi import APIRouter, status
from controllers import Controllers


router = APIRouter()

# router.get(
#         "/",
#         status_code=status.HTTP_200_OK
#         )(Controllers.root)


router.get(
        "/bdays/",
        status_code=status.HTTP_200_OK
        )(Controllers.list_birthdays)


router.post(
        "/bday/new",
        status_code=status.HTTP_201_CREATED
        )(Controllers.add_birthday)


router.put(
        "/bday/update",
        status_code=status.HTTP_202_ACCEPTED
        )(Controllers.update_birthday)


router.get(
        "/bday/get",
        status_code=status.HTTP_200_OK
        )(Controllers.get_birthday)


router.delete(
        "/bday/get",
        status_code=status.HTTP_204_NO_CONTENT
        )(Controllers.delete_birthday)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
router.post(
        "/auth/register",
        status_code=status.HTTP_201_CREATED
        )(Controllers.sign_up)


router.post(
        "/auth/login",
        status_code=status.HTTP_200_OK,
        )(Controllers.sign_in)


