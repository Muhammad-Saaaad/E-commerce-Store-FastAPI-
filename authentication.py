from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from fastapi import APIRouter , Depends , HTTPException , status , Request
from typing import Annotated
from database import db_dependency
import model , hashing , jwt_token
from jose import jwt , JWTError
# import jwt
import uvicorn

router = APIRouter(
    tags=['Authentication']
)

# SECRET_KEY = "505c8ad00a3da230699fd1191368a50acb956314bfb59cc49d6ec1fa898bbccb"
# ALGORITHM = "HS256"


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/signIn')


@router.post('/signIn', status_code = status.HTTP_202_ACCEPTED)
def user(db : db_dependency , req : OAuth2PasswordRequestForm = Depends() ):

    check_user = db.query(model.User).filter(model.User.username == req.username).first()

    if not check_user:
        raise HTTPException(status_code=404 , detail='Username not valid')
    
    check_pass = hashing.varify_pass(req.password , check_user.password)

    if not check_pass:
        raise HTTPException(status_code=404 , detail='password not valid')

    acess_token = jwt_token.create_acess_token(data={'sub':req.username , 'pass':req.password})

    return {'acess_token':acess_token , 'token_type':'bearer'}


def get_current_user(data : Annotated[str , Depends(oauth2_bearer)]):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)

    return jwt_token.verify_token(data , credentials_exception)


def get_token_from_header(request:Request, db:db_dependency):
    try:
        authorization: str = request.headers['token']
        if not authorization:
            raise HTTPException(status_code=400, detail="Authorization header is missing")
        token = authorization.split(" ")[1]
        print("token",token)
        payload = jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
        print("payload",payload)
        username : str = payload.get('sub')
        print(username)
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate user.")
        user = getUserByUsername(username=username,db=db)
        return user
    except Exception as e:
        print("error is",e)
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"{e}")

def getUserByUsername(username:str, db:db_dependency):
    return db.query(model.User).filter(model.User.username == username).first()


if __name__ == '__main__':
    uvicorn.run(router , host='0.0.0.0' , port=8000)