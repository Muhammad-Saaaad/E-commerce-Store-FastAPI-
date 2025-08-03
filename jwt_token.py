from datetime import timedelta , datetime
from jose import jwt , JWTError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def create_acess_token(data):
    to_encode = data.copy()
    time = datetime.utcnow() + timedelta(minutes=120)
    to_encode.update({'exp':time})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token :str , credientials):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data = {
        'username' : payload.get('sub'),
        'password' : payload.get('password')
        }
        if not data:
            raise credientials
        return data
    except JWTError:
        print('decodeing error')
        raise credientials
    

