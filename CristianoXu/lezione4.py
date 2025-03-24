from fastapi import FastAPI
import nest_asyncio
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "users" : 
        [
            {
                "id": 1,
                "name" : "Matteo"
            },  
            {
                "id": 2,
                "name" : "Marco"
            },
            {
                "id" : 3,
                "name": "Luigi"
            }
        ]     
    }

nest_asyncio.apply()

uvicorn.run(app, host = "127.0.0.1", port = 3000)