from fastapi import FastAPI
from src.models.simulator_models import TuringMachine

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Turing Machine API is running!"}

@app.post("/machine")
def create_machine(machine: TuringMachine):
    return machine



