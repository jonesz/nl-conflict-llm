#!/usr/bin/python
from typing import Literal, List, Optional
from pydantic import BaseModel, Field
import pytest


class FRETRequirement(BaseModel):
    """Requirement inputs go into the LLM, should come back looking like them aswell."""

    name: str = Field(pattern=r"^FSM\-[0-9]{3}$")


class ConflictBinary(BaseModel):
    """Corresponds to a test case where we only want "Conflict/No Conflict" """

    result: Literal["Conflict", "No Conflict"]
    reasoning: Optional[str] = None


class ConflictChoose(BaseModel):
    """Corresponds to a test case where we want both "Conflict/No Conflict" and a set
    of conflicting requirements."""

    result: Literal["Conflict", "No Conflict"]
    requirements: List[FRETRequirement]
    reasoning: Optional[str] = None


def test_FRETRequirement_passes():
    with pytest.raises(Exception):
        FRETRequirement(name="FSM003")

    FRETRequirement(name="FSM-003")
