from plantuml import PlantUML



plantuml_server = PlantUML(
    url="http://www.plantuml.com/plantuml/svg/"
)


def render_uml(plantuml_text: str):

    diagram_url = plantuml_server.get_url(plantuml_text)

    return diagram_url