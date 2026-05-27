from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI



load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0
)


BASE_PROMPT = """
You are an expert UML diagram generator.

Generate ONLY valid PlantUML.

STRICT RULES:
- Output ONLY PlantUML
- No explanations
- No markdown
- Start with @startuml
- End with @enduml
- Generate COMPLETE PlantUML only
- Do NOT use placeholders
- Do NOT use ellipsis (...)
- Ensure workflow is fully connected
- Output must be directly renderable
- Use valid PlantUML syntax only
- Keep diagrams visually readable
- Minimize crossing relationships
- Avoid excessive dependencies
- Group related components logically
- Prefer clarity over completeness
- Limit unnecessary associations
- Use layered architecture when appropriate
"""


DIAGRAM_GUIDELINES = {

    "sequence": """
Generate a UML Sequence Diagram.

Focus on:
- actors
- participants
- message flow
- request/response interactions
- activation/deactivation
- time ordering
- API/service interactions
- synchronous/asynchronous calls
""",

    "component": """
Generate a UML Component Diagram.

Focus on:
- services/modules
- databases
- external systems
- dependencies
- architecture boundaries
- interfaces between components
- layered architecture

Avoid sequence-style message flows.
""",

    "class": """
Generate a UML Class Diagram.

Focus on:
- classes
- attributes
- methods/functions
- inheritance
- associations
- aggregation/composition
- interfaces
- multiplicity relationships
- encapsulation
""",

    "activity": """
Generate a UML Activity Diagram.

Focus on:
- workflows
- actions
- decisions
- branching
- loops
- start/end nodes
- swimlanes if relevant
- parallel execution if needed
- object/data flow
""",

    "usecase": """
Generate a UML Use Case Diagram.

Focus on:
- actors
- use cases
- system goals
- actor-system interactions
- include/extend relationships
- system boundaries
""",

    "deployment": """
Generate a UML Deployment Diagram.

Focus on:
- servers
- cloud services
- containers
- databases
- execution environments
- deployment nodes
- infrastructure communication
- runtime topology
- Use node notation
- Use artifact notation
- Use valid PlantUML deployment syntax only
- Do not use container notation
""",

    "state": """
Generate a UML State Diagram.

Focus on:
- states
- transitions
- events
- lifecycle behavior
- entry/exit actions
- guards/conditions
- state changes
- Use [*] for start/end states
- Use --> for transitions
- Use valid PlantUML state syntax only
- Do not use activity or sequence notation
""",

    "object": """
Generate a UML Object Diagram.

Focus on:
- object instances
- runtime snapshots
- object relationships
- attribute values
- instantiated classes
""",

    "package": """
Generate a UML Package Diagram.

Focus on:
- namespaces
- module grouping
- package dependencies
- layered architecture
- subsystem organization
""",

    "communication": """
Generate a UML Communication Diagram.

Focus on:
- object/component interactions
- links between participants
- numbered message flow
- collaboration structure

Avoid timeline-heavy sequence notation.
""",

    "timing": """
Generate a UML Timing Diagram.

Focus on:
- state/value changes over time
- timing constraints
- lifeline state transitions
- duration representation
- real-time behavior
""",

    "interaction_overview": """
Generate a UML Interaction Overview Diagram.

Focus on:
- high-level interaction flow
- control flow between interactions
- activity-style orchestration
- interaction references
- workflow sequencing
""",

    "composite_structure": """
Generate a UML Composite Structure Diagram.

Focus on:
- internal structure
- ports
- connectors
- embedded components
- collaborations
- part relationships
""",

    "profile": """
Generate a UML Profile Diagram.

Focus on:
- stereotypes
- tagged values
- UML extensions
- domain-specific modeling
- constraints
- custom modeling semantics
"""
}


def generate_uml(user_prompt, refinement_notes, diagram_type, db):


    diagram_guideline = DIAGRAM_GUIDELINES.get(
        diagram_type,
        ""
    )

    prompt = f"""
{BASE_PROMPT}

Diagram Specific Guidelines:
{diagram_guideline}

Diagram Type:
{diagram_type}

Original Requirements:
{user_prompt}

Refinement Instructions:
{refinement_notes}
"""

    response = llm.invoke(prompt)

    return response.content