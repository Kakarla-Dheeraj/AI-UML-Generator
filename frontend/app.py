import streamlit as st
import requests


st.set_page_config(
    page_title="AI UML Generator",
    layout="wide"
)


st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0c10;
    color: #e6edf3;
}

.main-title {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 6px;
    color: #e6edf3;
}

.subtitle {
    font-size: 15px;
    color: #7d8590;
    margin-bottom: 30px;
}

.stTextInput input,
.stTextArea textarea {
    border-radius: 8px;
    border: 1px solid #30363d;
    background-color: #161b22;
    color: #e6edf3;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #58a6ff;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.1);
}

.stMultiSelect div {
    border-radius: 8px;
}

.stButton button {
    width: 100%;
    border-radius: 8px;
    height: 3.2em;
    font-size: 16px;
    font-weight: 600;
    background-color: #238636;
    color: white;
    border: none;
}

.stButton button:hover {
    background-color: #2ea043;
    color: white;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}

.diagram-card {
    padding: 24px;
    border-radius: 12px;
    background-color: #161b22;
    border: 1px solid #30363d;
    margin-bottom: 24px;
}

</style>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="main-title">🔷 AI UML Diagram Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Generate UML diagrams from software requirements using Gemini and PlantUML.</div>',
    unsafe_allow_html=True
)

st.divider()

with st.sidebar:

    st.header("UML Diagram Types")

    diagram_types = st.multiselect(
        "Select Diagrams",
        [
            "Sequence",
            "Component",
            "Class",
            "Usecase",
            "Activity",
            "Deployment",
            "State",
            "Package",
            "Object"
        ]
    )


username = st.text_input(
    "Enter Username"
)

load_project = False

if username:

    try:

        existing_response = requests.get(
            f"http://127.0.0.1:8000/project/{username}"
        )

        if existing_response.status_code == 200:

            existing_data = existing_response.json()

            if existing_data["exists"]:

                load_project = True

    except:

        pass


default_prompt = ""

if load_project:

    default_prompt = existing_data["prompt"]

col_left, col_right = st.columns([3, 2], gap="large")

with col_left:

    user_prompt = st.text_area(
        "Enter System Requirements",
        value=default_prompt,
        height=250,
    )

with col_right:

    refinement_notes = st.text_area(
        "Refinement Instructions",
        height=250,
        placeholder="""
Examples:
- Reduce clutter
- Add payment gateway
- Improve readability
- Add database interactions
- Show external API calls
"""
    )

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Generate UML Diagrams"):

    if not username:

        st.warning("Please enter username.")

    elif not user_prompt:

        st.warning("Please enter a prompt.")

    elif not diagram_types:

        st.warning("Please select at least one UML diagram type.")

    else:

        with st.spinner("Generating UML diagrams..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/generate",
                    json={
                        "username": username,
                        "prompt": user_prompt,
                        "refinement_notes": refinement_notes,
                        "diagram_types": diagram_types
                    },
                    timeout=300
                )

                if response.status_code == 200:

                    data = response.json()

                    diagrams = data["diagrams"]

                    st.success(
                        "UML diagrams generated successfully."
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.info(
                            f"User ID: {data['user_id']}"
                        )

                    for diagram_name, diagram_data in diagrams.items():

                        st.markdown(
                            '<div class="diagram-card">',
                            unsafe_allow_html=True
                        )

                        st.subheader(
                            f"{diagram_name.upper()} Diagram"
                        )

                        svg_viewer = f"""
<html>
<head>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: white; overflow: hidden; }}

  #toolbar {{
    position: fixed;
    top: 10px;
    right: 10px;
    display: flex;
    gap: 5px;
    z-index: 999;
  }}

  button {{
    width: 32px;
    height: 32px;
    border-radius: 6px;
    border: 1px solid #ccc;
    background: white;
    cursor: pointer;
    font-size: 16px;
  }}

  button:hover {{ background: #f0f0f0; }}

  #container {{
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: grab;
  }}

  #container:active {{ cursor: grabbing; }}

  #wrap {{
    transform-origin: center center;
  }}

  img {{
    display: block;
    max-width: none;
    user-select: none;
    pointer-events: none;
  }}
</style>
</head>
<body>

<div id="toolbar">
  <button id="zoomin">+</button>
  <button id="zoomout">−</button>
  <button id="reset" title="Reset">⊙</button>
</div>

<div id="container">
  <div id="wrap">
    <img src="{diagram_data['diagram_url']}">
  </div>
</div>

<script>
  const wrap = document.getElementById('wrap');
  const container = document.getElementById('container');

  let scale = 1, tx = 0, ty = 0;
  let dragging = false, startX, startY, startTx, startTy;

  function update() {{
    wrap.style.transform = `translate(${{tx}}px, ${{ty}}px) scale(${{scale}})`;
  }}

  container.addEventListener('wheel', (e) => {{
    e.preventDefault();
    scale = Math.min(Math.max(scale * (e.deltaY > 0 ? 0.9 : 1.1), 0.1), 10);
    update();
  }}, {{ passive: false }});

  container.addEventListener('mousedown', (e) => {{
    dragging = true;
    startX = e.clientX; startY = e.clientY;
    startTx = tx; startTy = ty;
  }});

  document.addEventListener('mousemove', (e) => {{
    if (!dragging) return;
    tx = startTx + (e.clientX - startX);
    ty = startTy + (e.clientY - startY);
    update();
  }});

  document.addEventListener('mouseup', () => {{ dragging = false; }});

  document.getElementById('zoomin').onclick  = () => {{ scale = Math.min(scale * 1.2, 10); update(); }};
  document.getElementById('zoomout').onclick = () => {{ scale = Math.max(scale * 0.8, 0.1); update(); }};
  document.getElementById('reset').onclick   = () => {{ scale = 1; tx = 0; ty = 0; update(); }};
</script>
</body>
</html>
"""

                        st.components.v1.html(
                            svg_viewer,
                            height=600,
                            scrolling=False
                        )

                        st.link_button(
                            "Open SVG in New Tab",
                            diagram_data["diagram_url"]
                        )

                        with st.expander(
                            "View PlantUML Source"
                        ):

                            st.code(
                                diagram_data["plantuml"],
                                language="text"
                            )

                        st.markdown(
                            '</div>',
                            unsafe_allow_html=True
                        )

                else:

                    st.error(
                        f"Backend Error: {response.status_code}"
                    )

                    try:

                        st.json(response.json())

                    except:

                        st.text(response.text)

            except requests.exceptions.Timeout:

                st.error(
                    "Request timed out while generating UML diagrams."
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to FastAPI backend."
                )

            except Exception as e:

                st.error(f"Error: {str(e)}")