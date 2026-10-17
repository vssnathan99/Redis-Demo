import json
from fastapi import FastAPI
from rd_client import redis_client

app=FastAPI()

users={
    1:{
        "id":101,
        "name":"Code",
        "email":"abc@gmail.com"
    }
    ,
    2:{
            "id":102,
            "name":"Solve",
            "email":"def@gmail.com"
        },
    3:{
            "id":103,
            "name":"Execute",
            "email":"ghi@gmail.com"
        }
}

@app.get("/")
async def root():
    return {"message":"FastAPI + Redis"}

@app.get("/health/redis")
async def redis_health():
    try:
        await redis_client.ping()
        return {"Message":"Redis Healthy"}
    except Exception:
        return {"Message":"Redis unHealthy"}
    
@app.get("/users/{user_id}")
async def get_user(user_id:int):
    cache_key=f"user:{user_id}"
    
    cached_data=await redis_client.get(cache_key)
    
    if cached_data:
        print("Cache Hit")
        return json.loads(cached_data)
    
    print ("cache miss")
    
    user=users.get(user_id)
    
    if not user:
        return {"message":"user not found"}
    
    await redis_client.set(
        cache_key,
        json.dumps(user),
        ex=15
    )
    return user