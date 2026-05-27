import requests
from plantuml import PlantUML


plantuml_server = PlantUML(
    url="https://www.plantuml.com/plantuml/svg/"
)


def validate_uml(plantuml_code: str):

    try:

        url = plantuml_server.get_url(plantuml_code)

        response = requests.get(url)

        svg_content = response.text

        if "Syntax Error" in svg_content:
            return False, svg_content

        return True, svg_content

    except Exception as e:

        return False, str(e)