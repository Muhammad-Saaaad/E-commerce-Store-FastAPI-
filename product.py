from fastapi import APIRouter , HTTPException , status  , Security
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from database import db_dependency
import schemas , model , hashing
from authentication import get_current_user
import uvicorn

router = APIRouter(
    prefix='/product',
    tags=['products'])

security = HTTPBearer()

@router.post('/insert', status_code=status.HTTP_201_CREATED)
async def insert_product(req : schemas.product_ins ,db : db_dependency , credentials : HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        current_user = get_current_user(token)
        
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials")
        
        get_user = db.query(model.User).filter(model.User.username == current_user.get('username')).first()

        product = model.Product(name = req.name , price = req.price , description = req.description , like_count = 0, user_id = get_user.id)
        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    except :
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
   
    
@router.get('/show_all' , response_model=list[schemas.all_products])
async def get_others_product(db : db_dependency , credentials : HTTPAuthorizationCredentials = Security(security)):

    try:
        token = credentials.credentials
        current_user = get_current_user(token)
        
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials")
        
        user = db.query(model.User).filter(model.User.username == current_user.get('username')).first()

        products = db.query(model.Product).filter(model.Product.user_id != user.id).all()

        return products

    except :
        HTTPException(status_code=404 , detail='not founded')


@router.put('/product_like' , status_code=status.HTTP_204_NO_CONTENT)
async def like_product(req : schemas.like_product , db : db_dependency , credentials : HTTPAuthorizationCredentials = Security(security)):
    
    try:
        token = credentials.credentials
        current_user = get_current_user(token)
        
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials")
    except :
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    # check if the product exists
    exists = db.query(model.Product).filter(model.Product.id == req.product_id).first()

    if not exists:
        raise HTTPException(status_code=404)
    
    # getting user's id

    get_user = db.query(model.User).filter(model.User.username == current_user.get('username')).first()

    #checking if id is already liked
    already_liked = db.query(model.Likes).filter(model.Likes.user_id == get_user.id , model.Likes.product_id == req.product_id).first()

    if already_liked:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED , detail='already liked')
    
    # adding the data into like table

    data = model.Likes(user_id = get_user.id , product_id = req.product_id)

    db.add(data)
    # adding the product
    exists.like_count = exists.like_count + 1
    db.commit()
    db.refresh(data)

    return


@router.put('/product_dislike' , status_code=status.HTTP_204_NO_CONTENT)
async def dislike_product(req : schemas.like_product , db : db_dependency , credentials : HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        current_user = get_current_user(token)
        
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials")
    except :
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    # check if the product exists
    exists = db.query(model.Product).filter(model.Product.id == req.product_id).first()

    if not exists:
        raise HTTPException(status_code=404)
    # getting user's id

    get_user = db.query(model.User).filter(model.User.username == current_user.get('username')).first()

    #checking if id is already liked
    already_liked = db.query(model.Likes).filter(model.Likes.user_id == get_user.id , model.Likes.product_id == req.product_id).first()

    if already_liked:
        # adding the data into like table

        # data = model.Likes(user_id = get_user.id , product_id = req.product_id)
        db.query(model.Likes).filter(model.Likes.user_id == get_user.id , model.Likes.product_id == req.product_id).delete(synchronize_session=False)

        exists.like_count = exists.like_count -1
        db.commit()

        return

    raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED)

@router.post('/add_to_cart' , status_code=200)
async def add_to_cart_product(req : schemas.product_crate , db : db_dependency , credentials : HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        current_user = get_current_user(token)
        
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials")
    except :
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    
    # getting the price of the product

    try:
        product = db.query(model.Product).filter(model.Product.id == req.product_id).first()

        print('product price ',product.price)

        total_price = req.quantity * product.price

        user = db.query(model.User).filter(model.User.username == current_user.get('username')).first()

        data = model.Shopping_Cart(user_id = user.id , product_id = req.product_id , quantity = req.quantity , total_price = total_price)

        db.add(data)
        db.commit()
        db.refresh(data)
        return 'data added to crate'
    except : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

if __name__ == '__main__':
    uvicorn.run(router , host='0.0.0.0' , port=8000)