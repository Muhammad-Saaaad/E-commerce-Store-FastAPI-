from fastapi import FastAPI
from database import engine
import model , user , authentication , product


app = FastAPI()

model.base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(product.router)