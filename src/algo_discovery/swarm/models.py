from typing import Literal

from pydantic import Field, model_validator

from ..schemas import MathSpecification, StrictModel

Requirement = Literal["problem", "equations", "circuit_plan", "measurement", "audit"]
REQUIREMENTS = ["problem", "equations", "circuit_plan", "measurement", "audit"]
# Placeholder that lets a contribution made before the equations contract validate;
# assemble() drops it, and the final specification is validated in full.
PENDING_EQUATIONS = "Equations are pending in a delegated contract."
PREREQUISITES = {
    "problem": set(),
    "equations": {"problem"},
    "circuit_plan": {"problem", "equations"},
    "measurement": {"problem", "equations", "circuit_plan"},
    "audit": {"problem", "equations", "circuit_plan", "measurement"},
}
FIELDS = {
    "problem": ["problem", "reconstruction_scope"],
    "equations": ["symbols", "equations"],
    "circuit_plan": ["registers", "initial_state", "steps"],
    "measurement": ["measurement", "classical_postprocessing"],
    "audit": list(MathSpecification.model_fields),
}


class Genotype(StrictModel):
    preferences: dict[str, float]
    bid_fraction: float = Field(default=0.2, ge=0.05, le=0.3)
    max_parts: int = Field(default=2, ge=1, le=2)
    effort: Literal["low", "medium", "high"] = "medium"
    max_tokens: int = Field(default=6144, ge=2048, le=8192)

    @model_validator(mode="after")
    def check_preferences(self):
        if set(self.preferences) != set(REQUIREMENTS) or any(
            not 0.1 <= score <= 1 for score in self.preferences.values()
        ):
            raise ValueError("Each requirement needs a finite capability score from 0.1 to 1.")
        return self


def initial_genotypes() -> list[Genotype]:
    return [
        Genotype(
            preferences={
                "problem": 1.0,
                "equations": 1.0,
                "circuit_plan": 0.55,
                "measurement": 0.5,
                "audit": 0.6,
            }
        ),
        Genotype(
            preferences={
                "problem": 0.6,
                "equations": 0.65,
                "circuit_plan": 1.0,
                "measurement": 1.0,
                "audit": 0.6,
            }
        ),
        Genotype(
            preferences={
                "problem": 0.5,
                "equations": 0.6,
                "circuit_plan": 0.6,
                "measurement": 0.65,
                "audit": 1.0,
            }
        ),
    ]


class Contribution(StrictModel):
    completed_requirements: list[Requirement]
    specification: MathSpecification
    child_groups: list[list[Requirement]]
    changes: list[str]
    summary: str = Field(min_length=1, max_length=2000)
