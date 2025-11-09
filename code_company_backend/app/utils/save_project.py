# app/utils/save_project.py
import json
from pathlib import Path
from datetime import datetime

PROJECTS_FILE = Path("app/data/projects.json")

def _read_projects():
    if PROJECTS_FILE.exists():
        try:
            return json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def _write_projects(data):
    PROJECTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROJECTS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def append_project(project_obj):
    """
    Insert new project at start (newest first).
    project_obj should be a dict with at least 'title' and 'status'.
    """
    data = _read_projects()
    data.insert(0, project_obj)
    _write_projects(data)
    return project_obj

def get_all_projects():
    return _read_projects()
