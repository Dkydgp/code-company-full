import requests
from config import Config
from app.utils.json_handler import write_memory, read_memory
from app.utils.search_api import search_project


def find_coding_problem():
    """Technical Manager: Finds an unsolved or tricky coding project idea."""
    print("🔍 Technical Manager: Searching for coding projects...")

    # Step 1: Define what to search for
    query = "interesting Python automation project ideas OR open source Python projects to build"

    # Step 2: Perform web search using Serper.dev
    try:
        results = search_project(query)
    except Exception as e:
        print(f"⚠️ Error while searching: {e}")
        return {"status": "error", "message": str(e)}

    if not results:
        print("⚠️ No search results returned.")
        return {"status": "error", "message": "No results found from Serper.dev."}

    # Step 3: Safely handle the first valid result
    project = results[0]

    # ✅ Handle missing fields gracefully
    title = project.get("title", "Untitled Project")
    snippet = project.get("snippet", "No description available.")
    link = project.get("link") or project.get("url") or "#"

    # Step 4: Prepare project summary for CEO
    project_summary = {
        "project_title": title.strip(),
        "problem_summary": snippet.strip(),
        "source_link": link.strip(),
        "status": "Pending CEO Review"
    }

    # Step 5: Save to memory.json
    try:
        data = read_memory()

        # ✅ Always overwrite under 'current_project' (standard key)
        data["current_project"] = project_summary

        # Optional tracking info
        data["last_action"] = "technical_search"
        write_memory(data)

        print("✅ Technical Manager: Project identified and saved to memory.json under 'current_project'.")
    except Exception as e:
        print(f"⚠️ Error writing to memory: {e}")
        return {"status": "error", "message": f"Failed to save project: {e}"}

    return {
        "status": "success",
        "message": "Technical Manager found a project",
        "project": project_summary
    }
