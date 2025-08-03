from fastapi import APIRouter , status , HTTPException , Depends , Request , Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import hashing , schemas , model
from database import db_dependency
from authentication import get_current_user , get_token_from_header
from typing import List

router = APIRouter(
    tags=['user']
)
security = HTTPBearer()


@router.post('/insert', status_code=status.HTTP_201_CREATED)
async def insert_user(req : schemas.user_ins , db : db_dependency):
    check = db.query(model.User).filter(model.User.username == req.username).first()

    if check:
       raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE , detail='username already exists:')
    
    data = model.User(username = req.username , password = hashing.encrypt_pss(req.password))

    db.add(data)
    db.commit()
    db.refresh(data)
    return {'detail' :'data inserted sucessfully' }



@router.get('/get_user' , response_model=List[schemas.user_ins])
async def get_users(request:Request,db : db_dependency , credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        current_user = get_current_user(token)
        
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        users = db.query(model.User).all()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

# @router.delete('/delete' , status_code= status.HTTP_204_NO_CONTENT)
# async def del_user(req : schemas.user_ins , db : db_dependency , credentials: HTTPAuthorizationCredentials = Security(security)):

#     try:
#         token = credentials.credentials
#         current_user = get_current_user(token)
            
#         if not current_user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials"
#             )

#         delete = db.query(model.User).filter(model.User.username == req.username).delete(synchronize_session=False)
#         if delete:
#             print('before commit')
#             db.commit()
#             print('after commit')
#             return
        
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=str(e))


# if __name__ == '__main__':
#     uvicorn.run(router , host='0.0.0.0' , port=8000)