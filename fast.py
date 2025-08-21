from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from workflow import Workflow
from typing import Dict, Any
import warnings

warnings.filterwarnings("ignore")

app = FastAPI()

class InputData(BaseModel):
    data: Dict[str, Any]

@app.post("/predict")
async def predict(inputs: InputData):
    try:
        work = Workflow()
        response = work.execute(inputs.data)  

        if isinstance(response, dict):
            return {"predictions": response.get("answer", None)}
        else:
            return {"predictions": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
