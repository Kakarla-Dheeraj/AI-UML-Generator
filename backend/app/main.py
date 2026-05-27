from fastapi import FastAPI
from fastapi import Depends

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.services.uml_renderer import render_uml

from app.database.database import engine
from app.database.database import get_db

from app.database.models import Base
from app.database.models import User
from app.database.models import Project
from app.database.models import UMLGeneration

from app.graph.uml_graph import uml_graph


app = FastAPI()

Base.metadata.create_all(bind=engine)


class UMLRequest(BaseModel):

    username: str

    prompt: str

    refinement_notes: str

    diagram_types: list[str]


@app.post("/generate")
def generate_diagram(
    request: UMLRequest,
    db: Session = Depends(get_db)
):

    results = {}

    user = db.query(User).filter(
        User.username == request.username
    ).first()

    if not user:

        user = User(
            username=request.username
        )

        db.add(user)

        db.commit()

        db.refresh(user)

    project = db.query(Project).filter(
        Project.user_id == user.id
    ).order_by(Project.id.desc()).first()

    if not project:

        project = Project(
            title="Generated UML Project",
            prompt=request.prompt,
            refinement_notes=request.refinement_notes,
            user_id=user.id
        )

        db.add(project)

        db.commit()

        db.refresh(project)

    else:

        project.prompt = request.prompt

        project.refinement_notes = request.refinement_notes

        db.commit()

        db.query(UMLGeneration).filter(
            UMLGeneration.project_id == project.id
        ).delete()

        db.commit()

    for diagram_type in request.diagram_types:

        graph_result = uml_graph.invoke({

            "user_prompt": request.prompt,

            "refinement_notes": request.refinement_notes,

            "diagram_type": diagram_type,

            "uml_code": "",

            "is_valid": False,

            "validation_error": "",

            "retry_count": 0,

            "db": db
        })

        plantuml_output = graph_result["uml_code"]

        if not graph_result["is_valid"]:

            plantuml_output = f"""
@startuml
title Failed to Generate Valid {diagram_type} Diagram

note "Unable to generate valid UML after retries." as N1

@enduml
"""

        diagram_url = render_uml(plantuml_output)

        uml_record = UMLGeneration(
            project_id=project.id,
            diagram_type=diagram_type,
            plantuml=plantuml_output,
            diagram_url=diagram_url
        )

        db.add(uml_record)

        results[diagram_type] = {
            "plantuml": plantuml_output,
            "diagram_url": diagram_url
        }

    db.commit()

    return {
        "user_id": user.id,
        "project_id": project.id,
        "diagrams": results
    }

@app.get("/project/{username}")
def get_project(
    username: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:

        return {
            "exists": False
        }

    project = db.query(Project).filter(
        Project.user_id == user.id
    ).order_by(Project.id.desc()).first()

    if not project:

        return {
            "exists": False
        }

    umls = db.query(UMLGeneration).filter(
        UMLGeneration.project_id == project.id
    ).all()

    diagrams = {}

    for uml in umls:

        diagrams[uml.diagram_type] = {
            "plantuml": uml.plantuml,
            "diagram_url": uml.diagram_url
        }

    return {
        "exists": True,
        "project_id": project.id,
        "prompt": project.prompt,
        "diagrams": diagrams
    }