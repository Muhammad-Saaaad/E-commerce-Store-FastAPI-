from pydantic import BaseModel

class user_ins(BaseModel):
    username :str
    password :str

    class Config:
        from_attributes = True

class product_ins(BaseModel):
    name:str
    description : str
    price : float

    class Config:
        from_attributes=True

class all_products(BaseModel):
    id :int
    name:str
    description : str
    price : float
    like_count : int
    user_id : int 

    class Config:
        from_attributes = True

class product_crate(BaseModel):
    product_id : int
    quantity : int

class like_product(BaseModel):
    product_id : int

    class Config:
        from_attributes=True