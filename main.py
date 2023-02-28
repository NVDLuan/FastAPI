from fastapi import FastAPI, Body, Depends
from model import PostSchema, UserSchema, UserLoginSchema
from auth.jwt_hander import signJWT
from auth.jwt_bearer import jwtBearer

app = FastAPI()


posts = [
    {
        "id": '1',
        "tilte": "sadfads",
        "content": "adsfaadsfndsfakfafidaksdjfasdf"
    },
    {
        "id": '2',
        "tilte": "laufaasndf",
        "content": "asdlfakjsdkfautkeatujoewiwq c"
    },
{
        "id": '3',
        "tilte": "ladufadfn",
        "content": "asdk sdfkladsfkajsdf adsfjadsfj  c"
    }

]

users=[]

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/posts")
async  def getPost():
    return {"data": posts}

@app.get("/posts/{id}")
async def getOnePost(id: int):
    if(id>len(posts)):
        return {"error":" loi roio"}
    return {"data": posts[id]}

@app.post("/posts", dependencies=[Depends(jwtBearer())])
async def createPost(post:PostSchema):
    post.id = len(posts)+1
    posts.append(post)
    return {
        "info": "Post added"
    }

@app.post("/user/signup")
def createUser(user:UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)


def checkUser(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
             return True
        else: return False

@app.post("/user/login")
def loginUser(user: UserLoginSchema = Body(default= None)):
    if checkUser(user):
        return signJWT(user.email)
    return {
        'message': "invalid login detail"
    }