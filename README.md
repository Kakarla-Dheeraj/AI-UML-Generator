# AI UML Diagram Generator

## Overview

AI UML Diagram Generator is a full-stack AI-powered platform that generates UML diagrams from natural language software requirements using Gemini, LangGraph, FastAPI, Streamlit, and PlantUML.

The platform allows users to:

- Generate multiple UML diagram types from a single software design prompt
- Render UML diagrams dynamically on a web UI
- Validate PlantUML syntax automatically
- Retry invalid generations using LangGraph workflow orchestration
- Persist users and projects using SQLite
- Allow existing users to iteratively refine and update their UML diagrams
- Store project history and UML generations

---

# Assignment Requirements Covered

## Input Format

Example request:

```json
{
  "prompt": "I am working on a compliance monitoring solution which will pull in the latest circulars from SEBI and parse them...",
  "diagram_types": ["sequence", "component", "class"]
}
```

---

# Supported UML Diagram Types

- Sequence Diagram
- Component Diagram
- Class Diagram
- Use Case Diagram
- Activity Diagram
- Deployment Diagram
- State Diagram
- Package Diagram
- Object Diagram

---

# Tech Stack

## Backend

- FastAPI
- LangGraph
- LangChain
- Gemini 2.5 Flash
- PlantUML
- SQLite
- SQLAlchemy

## Frontend

- Streamlit

---

# System Architecture

```text
User Prompt
    ↓
Streamlit Frontend
    ↓
FastAPI Backend
    ↓
LangGraph Workflow
    ↓
Gemini UML Generation
    ↓
PlantUML Syntax Validation
    ↓
Retry Loop (if invalid)
    ↓
PlantUML Rendering
    ↓
SVG Diagram Output
    ↓
SQLite Persistence Layer
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repo-url>
cd <repo-folder>
```

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

## 3. Activate Virtual Environment

### Linux / Mac

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

## 6. Start Backend

```bash
uvicorn app.main:app --reload
```

## 7. Start Frontend

```bash
streamlit run app.py
```

---

# Key Features

- Multi-UML generation
- LangGraph workflow orchestration
- Automatic syntax validation
- SVG UML rendering
- Persistent users/projects
- Iterative prompt refinement
- Retry-based recovery pipeline

---

# Conclusion

This project demonstrates a production-style AI workflow system for automated UML generation using LLMs, workflow orchestration, syntax validation, and persistent project management.
