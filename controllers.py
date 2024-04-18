from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import *
from schemas import *
from typing import Annotated, List
from mongoengine import NotUniqueError, DoesNotExist

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Controllers:
    
    def root(token: Annotated[str, Depends(oauth2_scheme)]):
        return {"token": token}
        # return {"message": "ROOT ENDPOINT"}


    fake_users_db = {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "fakehashedsecret",
            "disabled": False,
        },
        "alice": {
            "username": "alice",
            "full_name": "Alice Wonderson",
            "email": "alice@example.com",
            "hashed_password": "fakehashedsecret2",
            "disabled": True,
        },
    }

    def fake_hash_password(password: str):
        return "fakehashed" + password

    class User(BaseModel):
        username: str
        email: Union[str, None] = None
        full_name: Union[str, None] = None
        disabled: Union[bool, None] = None


    class UserInDB(User):
        hashed_password: str


    def get_user(db, username: str):
        if username in db:
            user_dict = db[username]
            return Controllers.UserInDB(**user_dict)


    def fake_decode_token(token):
        # This doesn't provide any security at all
        # Check the next version
        user = Controllers.get_user(Controllers.fake_users_db, token)
        return user


    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        user = Controllers.fake_decode_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user


    async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user


    async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        user_dict = Controllers.fake_users_db.get(form_data.username)
        if not user_dict:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        user = Controllers.UserInDB(**user_dict)
        hashed_password = Controllers.fake_hash_password(form_data.password)
        if not hashed_password == user.hashed_password:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        return {"access_token": user.username, "token_type": "bearer"}


    async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ):
        return current_user














    def list_birthdays() -> List[PersonResponseSchema]:
        data = Person.objects.all()
        bday_data = []
        for bd in data:
            bday_data.append(
                {"name": bd.name,
                 "birth_date": bd.birth_date,
                 "extra_info": bd.extra_info,
                 "id": str(bd.id)}
            )
        return bday_data
    
    def add_birthday(data: PersonCreateSchema):
        try:
            new_data = Person(name=data.name, birth_date=data.birth_date, extra_info=data.extra_info)
            new_data.save()
            return {"message": "Data created successfully"}
        except NotUniqueError:
            raise HTTPException(status_code=406, detail="Data not unique")
        
    
    def update_birthday(data_id: str, data: PersonUpdateSchema):
        try:
            update_data = data.model_dump(exclude_unset=True)
            Person.objects(id=data_id).update(**update_data)
            return {"message": "Data successfully updated"}
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Data not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    
    def get_birthday(data_id: str) -> PersonResponseSchema:
        try:
            person = Person.objects.get(id=data_id)
            person_data = {
            "name": person.name,
            "birth_date": person.birth_date,
            "extra_info": person.extra_info,
            "id": str(person.id)
            }
        except Exception:
            raise HTTPException(status_code=404, detail="Data not found")
        return person_data
    
    
    def delete_birthday(data_id: str):
        try:
            data = Person.objects.get(id=data_id)
            data.delete()
        except Exception:
            raise HTTPException(status_code=404, detail="Data not found")
        return {"message": "Data deleted successfully"}     
        


        
