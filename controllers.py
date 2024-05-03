
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import *
from schemas import *
from typing import Annotated, List, Union
from mongoengine import NotUniqueError, DoesNotExist
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import datetime
import settings
from logging import getLogger


logger = getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")




class Controllers:

    def sign_up(payload: AccountRegSchema):
        try:
            hashed_password = pwd_context.hash(payload.hashed_password)
            data = BaseAccount(
                username=payload.username,
                hashed_password=hashed_password,
                email=payload.email
            )
            data.save()
            return {"message": "User created successfully"}
        except NotUniqueError:
            raise HTTPException(
                status_code=406,
                detail="Data not unique"
            )

#   data: Annotated[OAuth2PasswordRequestForm, Depends()]
    def sign_in(payload: Signin_Schema):
        
        try:
            user = BaseAccount.objects.get(username=payload.username)
            if user and Controllers.verify_password(payload.password, user.hashed_password):
                access_token = Controllers.jwt_encode(data={"sub": user.username})
        except:
            raise HTTPException(
                status_code=404,
                detail="Details not found"
            )
        response = JSONResponse(
            {
                "user": {
                    # "id": str(data.id),
                    "username": payload.username,
                    "email": payload.email,
                }
            }
        )
        response.set_cookie(
            key="token",
            value=access_token,
            secure=True,
            samesite="none",
            expires=(
                datetime.datetime.utcnow()
                + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            ).strftime("%a, %d %b %Y %H:%M:%S GMT"),
        )
        return response
        # return {"access_token": access_token,
        #         "token_type": "bearer"
        # }


    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(
            plain_password,
            hashed_password
        )
        

    def jwt_encode(data: dict):
        return jwt.encode(
            {
                **data,
                "exp": datetime.datetime.now(datetime.UTC)
                + timedelta(minutes=20)
            },
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )


    def jwt_decode(token: str):
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Could not decode token"
            )
        
    # token: Annotated[str, Depends(oauth2_scheme)]
    async def auth_account(request: Request = Annotated[Request, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        """Checks authentication"""
        token = request.cookies.get("token")
        if token is None:
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        try:
            payload  = Controllers.jwt_decode(token)
        except Exception:
            logger.exception("auth_account(jwt_decode): Detokenization failed")
            raise HTTPException(
                headers={"WWW-Authenticate": "Bearer"},
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        try:
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
    

    def list_birthdays(user: BaseAccount = Depends(auth_account))-> List[PersonResponseSchema]:
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
    

    def list_users()-> List[AccountResponseSchema]:
        user = BaseAccount.objects.all()
        users = []
        for _ in user:
            users.append(
                {
                    "username": _.username,
                    "email": _.email
                }
            )
        return users
    
    
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
        

