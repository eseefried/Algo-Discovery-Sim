"""Local API for block one. Do not expose a credential-backed endpoint publicly."""

from fastapi import FastAPI, HTTPException

from .config import ConfigurationError, Settings
from .equations import GenerationError, generate_equations
from .schemas import EquationRequest, EquationResult

app = FastAPI(title="Algo Discovery: Abstract to Equations", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "block": "abstract_to_equations"}


@app.post("/equations", response_model=EquationResult)
def equations(request: EquationRequest):
    try:
        return generate_equations(request, Settings.from_env())
    except ConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from None
    except GenerationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from None
    except OSError:
        raise HTTPException(status_code=500, detail="Unable to save run artifacts.") from None
