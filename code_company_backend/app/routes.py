from flask import Blueprint, request, jsonify, current_app
from app.utils.json_handler import save_to_json, read_json
from app.utils.search_api import search
from app.models.technical import find_coding_problem
from app.models.ceo import ceo_decision
from app.models.operations import execute_project
from app.utils.supabase_logger import log_project_run, fetch_project_history
from app.utils.save_project import append_project
import time
from datetime import datetime

main = Blueprint("main", __name__)

# 🏠 HOME ROUTE
@main.route("/", methods=["GET"])
def home():
    """Health check route."""
    return jsonify({
        "message": "🏗️ Welcome to Code Company Backend API!",
        "available_routes": [
            "/api/test",
            "/api/projects",
            "/search",
            "/save",
            "/read",
            "/technical/search",
            "/ceo/decision",
            "/operations/execute",
            "/company/run",
            "/company/history"
        ]
    }), 200


# 💾 SAVE DATA
@main.route("/save", methods=["POST"])
def save_data():
    """Saves custom JSON data to local memory.json file."""
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400

    try:
        result = save_to_json(data)
        return jsonify({
            "status": "success",
            "message": "Data saved successfully",
            "data": result
        }), 201
    except Exception as e:
        current_app.logger.exception("Save data error")
        return jsonify({"status": "error", "message": str(e)}), 500


# 📂 READ SAVED DATA
@main.route("/read", methods=["GET"])
def read_data():
    """Fetches all stored JSON data from memory.json."""
    try:
        data = read_json()
        return jsonify({
            "status": "success",
            "data": data
        }), 200
    except Exception as e:
        current_app.logger.exception("Read data error")
        return jsonify({"status": "error", "message": str(e)}), 500


# 🔍 SEARCH (SERPER API)
@main.route("/search", methods=["GET", "POST"])
def search_route():
    """Runs a Serper.dev search."""
    if request.method == "GET":
        query = request.args.get("q")
    else:
        body = request.get_json() or {}
        query = body.get("query")

    if not query:
        return jsonify({"status": "error", "message": "Missing query parameter"}), 400

    try:
        results = search(query)
        save_to_json({
            "type": "search",
            "query": query,
            "count": len(results)
        })
        return jsonify({
            "status": "success",
            "query": query,
            "results": results
        }), 200
    except Exception as e:
        current_app.logger.exception("Search error")
        return jsonify({"status": "error", "message": str(e)}), 500


# 🤖 TECHNICAL MANAGER — PROJECT FINDER
@main.route("/technical/search", methods=["GET"])
def technical_search():
    """Triggers the Technical Manager AI to find one unsolved or tricky coding problem."""
    try:
        result = find_coding_problem()
        if isinstance(result, dict) and "status" in result:
            return jsonify(result), 200
        else:
            return jsonify({
                "status": "success",
                "message": "Technical Manager found a project",
                "project": result
            }), 200
    except Exception as e:
        current_app.logger.exception("Technical Manager error")
        return jsonify({"status": "error", "message": str(e)}), 500


# 👑 CEO — DECISION MAKER
@main.route("/ceo/decision", methods=["POST"])
def ceo_route():
    """Triggers the CEO AI to make a decision on the current project."""
    try:
        data = request.get_json(silent=True) or {}
        user_prompt = data.get("prompt")
        result = ceo_decision(user_prompt=user_prompt)
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.exception("CEO decision error")
        return jsonify({"status": "error", "message": str(e)}), 500


# ⚙️ OPERATIONS MANAGER — PROJECT EXECUTION
@main.route("/operations/execute", methods=["POST"])
def operations_execute():
    """Runs the Operations Manager AI to execute the approved project."""
    try:
        result = execute_project()
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.exception("Operations execution error")
        return jsonify({"status": "error", "message": str(e)}), 500


# 🏢 FULL COMPANY WORKFLOW — AUTO EXECUTION + SUPABASE LOGGING
@main.route("/company/run", methods=["GET"])
def company_run():
    """
    Runs the full AI company workflow automatically:
    1️⃣ Technical Manager searches for a project.
    2️⃣ CEO (OPENAI) reviews and approves/rejects.
    3️⃣ Operations Manager executes if approved.
    4️⃣ Logs results to Supabase and local file.
    """
    try:
        workflow_log = {}

        # 1️⃣ Technical Phase
        print("\n🚀 Starting Technical Manager phase...")
        technical_result = find_coding_problem()
        workflow_log["technical"] = technical_result

        # 2️⃣ CEO Phase
        print("\n👑 Starting CEO decision phase...")
        ceo_result = ceo_decision(
            user_prompt="Approve only Python or automation-based projects"
        )
        workflow_log["ceo"] = ceo_result

        # 3️⃣ Operations Phase
        print("\n⚙️ Starting Operations Manager phase...")
        if ceo_result.get("decision") == "approve":
            operations_result = execute_project()
        else:
            operations_result = {
                "status": "skipped",
                "message": "Project not approved by CEO."
            }
        workflow_log["operations"] = operations_result

        # 4️⃣ Log to Supabase
        print("\n🗄️ Logging company run to Supabase...")
        try:
            log_project_run(
                project_title=technical_result.get("project", {}).get("project_title", "N/A"),
                ceo_decision=ceo_result.get("decision", "N/A"),
                ceo_reason=ceo_result.get("reason", "N/A"),
                operations_status=operations_result.get("status", "N/A")
            )
            print("✅ Supabase log entry created successfully.")
        except Exception as log_err:
            print(f"⚠️ Supabase logging failed: {log_err}")

        # 5️⃣ Append to Local File for Frontend
        from app.utils.save_project import append_project
        import time
        from datetime import datetime

        project_record = {
            "id": int(time.time()),
            "title": operations_result.get("project_title") or technical_result.get("project", {}).get("project_title", "Untitled Project"),
            "summary": operations_result.get("solution_summary") or "",
            "details_markdown": operations_result.get("final_code") or "",
            "status": operations_result.get("status", "unknown"),
            "executed_at": datetime.utcnow().isoformat() + "Z",
            "source": technical_result.get("project", {}).get("source_link", "")
        }

        try:
            append_project(project_record)
            print("✅ Project appended to app/data/projects.json")
        except Exception as e:
            print(f"⚠️ Failed to append project to file: {e}")

        # 6️⃣ Final Response
        return jsonify({
            "status": "completed",
            "company": "Code Company (Beta)",
            "summary": {
                "technical": {
                    "project_title": technical_result.get("project", {}).get("project_title", "N/A"),
                    "status": technical_result.get("project", {}).get("status", "N/A")
                },
                "ceo": {
                    "decision": ceo_result.get("decision", "N/A"),
                    "reason": ceo_result.get("reason", "N/A")
                },
                "operations": {
                    "status": operations_result.get("status", "N/A"),
                    "message": operations_result.get("message", "N/A")
                }
            },
            "details": workflow_log
        }), 200

    except Exception as e:
        current_app.logger.exception("Company workflow error")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# 🗂️ COMPANY PROJECT HISTORY — FETCH FROM SUPABASE
@main.route("/company/history", methods=["GET"])
def company_history():
    """Fetch all project run logs stored in Supabase (latest first)."""
    try:
        print("\n📜 Fetching project history from Supabase...")
        result = fetch_project_history()

        if result["status"] == "success":
            print(f"✅ Retrieved {len(result['data'])} project entries from Supabase.")
            return jsonify({
                "status": "success",
                "count": len(result["data"]),
                "projects": result["data"]
            }), 200
        else:
            print(f"⚠️ Error fetching project history: {result['message']}")
            return jsonify({
                "status": "error",
                "message": result["message"]
            }), 500

    except Exception as e:
        current_app.logger.exception("History fetch error")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 🧪 BASIC TEST ROUTE FOR FRONTEND CONNECTIVITY
@main.route("/api/test", methods=["GET"])
def test():
    """Simple API test endpoint."""
    return jsonify({"message": "✅ Hello from Flask Backend!"}), 200


# 📁 PROJECTS API (For Frontend)
@main.route("/api/projects", methods=["GET"])
def api_projects():
    """Return projects list from app/data/projects.json (newest first)."""
    try:
        from app.utils.save_project import get_all_projects
        projects = get_all_projects()
        return jsonify({"status": "success", "projects": projects}), 200
    except Exception as e:
        current_app.logger.exception("Error reading projects file")
        return jsonify({"status": "error", "message": str(e)}), 500

