from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END

from app.services.uml_generator import generate_uml
from app.services.uml_validator import validate_uml


class UMLState(TypedDict):

    user_prompt: str

    refinement_notes: str

    diagram_type: str

    uml_code: str

    is_valid: bool

    validation_error: str

    retry_count: int

    db: object
    


def generate_node(state):

    uml_code = generate_uml(
        user_prompt=state["user_prompt"],
        refinement_notes=state["refinement_notes"],
        diagram_type=state["diagram_type"],
        db=state["db"]
    )

    state["uml_code"] = uml_code

    state["retry_count"] += 1

    return state


def validate_node(state):

    is_valid, result = validate_uml(
        state["uml_code"]
    )

    state["is_valid"] = is_valid

    state["validation_error"] = result

    return state


def validation_router(state):

    if state["is_valid"]:

        return "valid"

    if state["retry_count"] >= 3:

        return "failed"

    return "invalid"


graph_builder = StateGraph(UMLState)

graph_builder.add_node(
    "generate",
    generate_node
)

graph_builder.add_node(
    "validate",
    validate_node
)

graph_builder.set_entry_point(
    "generate"
)

graph_builder.add_edge(
    "generate",
    "validate"
)

graph_builder.add_conditional_edges(
    "validate",
    validation_router,
    {
        "valid": END,
        "invalid": "generate",
        "failed": END
    }
)

uml_graph = graph_builder.compile()