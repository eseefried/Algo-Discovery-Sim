"""Local API for the math and code blocks."""

from fastapi import FastAPI, HTTPException

from .code_generation import generate_code
from .code_schemas import CodeRequest, CodeResult
from .config import ConfigurationError, Settings
from .equations import GenerationError, generate_equations
from .schemas import EquationRequest, EquationResult

app = FastAPI(title="Algo Discovery: Abstract to Qiskit", version="0.2.0")


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


@app.post("/qiskit", response_model=CodeResult)
def qiskit_code(request: CodeRequest):
    try:
        return generate_code(request, Settings.from_env())
    except ConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from None
    except GenerationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from None
    except OSError:
        raise HTTPException(status_code=500, detail="Unable to save code artifacts.") from None
