#Validare una password sicura
from pydantic import BaseModel, validator  

class UserPassword(BaseModel):  
    password: str  

    @validator('password')  
    def validate_password(cls, v):  
        if len(v) < 8:  
            raise ValueError("La password deve avere almeno 8 caratteri")  
        if not any(char.islower() for char in v):  
            raise ValueError("La password deve contenere almeno una lettera minuscola")  
        if not any(char.isupper() for char in v):  
            raise ValueError("La password deve contenere almeno una lettera maiuscola")  
        if not any(char.isdigit() for char in v):  
            raise ValueError("La password deve contenere almeno un numero")  
        if not any(not char.isalnum() for char in v):  
            raise ValueError("La password deve contenere almeno un carattere speciale")  
        
        return v  

try:  
    valid_password = UserPassword(password="Abc123$%")  
    print(valid_password)  
except ValueError as e:  
    print(f"Errore di validazione: {e}")  

try:  
    invalid_password = UserPassword(password="abcdeG98")  
    print(invalid_password)  
except ValueError as e:  
    print(f"Errore di validazione: {e}")   


#Creazione di un 'API per gestire utenti
from fastapi import FastAPI
from pydantic import BaseModel
import nest_asyncio
import uvicorn

app = FastAPI()

user_list = []

class Utente(BaseModel):
    nome : str
    email : str

@app.post("/utente/")
async def create_user (user : Utente):
    user_list.append({"nome" : user.nome, "email" : user.email})

@app.get("/")
async def root ():
    return {"users" : user_list}

nest_asyncio.apply()
uvicorn.run(app, host = "127.0.0.1", port = 8000)