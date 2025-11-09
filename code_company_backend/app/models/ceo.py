import requests
import json
import re
from config import Config
from app.utils.json_handler import read_memory, write_memory


def ceo_decision(user_prompt=None):
    """
    CEO AI (OPENAI V3.1):
    Reviews the current project and decides whether to approve or reject it.
    Auto-approves if: no project is found OR project involves Python.
    Otherwise, consults OPENAI V3.1 through OpenRouter.
    """

    data = read_memory()
    project = data.get("current_project")

    # 1️⃣ No active project → auto-approve
    if not project:
        print("⚙️ No project found. CEO auto-approving idle workload.")
        result = {
            "decision": "approve",
            "reason": "No active project found. Approving to start new work."
        }

    else:
        title = project.get("project_title", "").lower()
        summary = project.get("problem_summary", "").lower()

        # 2️⃣ Auto-approve if Python-related
        if "python" in title or "python" in summary:
            print("🐍 Python-based project detected — auto-approved.")
            result = {
                "decision": "approve",
                "reason": "The project involves Python coding — approved."
            }

        # 3️⃣ Otherwise — ask OPENAI V3.1 via OpenRouter
        else:
            print("🧠 Non-Python project detected — consulting openai/gpt-oss-20b CEO AI.")
            prompt = f"""
            You are the CEO of Code Company.
            Evaluate this project proposal and decide whether to approve or reject it.

            Project Title: {project.get('project_title')}
            Summary: {project.get('problem_summary')}
            Source: {project.get('source_link')}

            Rules:
            - Approve only if the project involves Python code, coding implementation, or automation.
            - Reject if it is theoretical or unrelated to coding.
            - Respond STRICTLY in JSON format, nothing else:
              {{
                "decision": "approve" or "reject",
                "reason": "short explanation"
              }}
            """

            try:
                headers = {
                    "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": "openai/gpt-oss-20b:free",  # ✅ OPEANI V3.1 on OpenRouter
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a logical, concise CEO AI using openai/gpt-oss-20b "
                                "Respond ONLY in valid JSON format. No text outside JSON."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ]
                }

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                response.raise_for_status()
                ai_reply = response.json()["choices"][0]["message"]["content"]

                # 🧩 Extract JSON even if extra text is present
                match = re.search(r"\{.*\}", ai_reply, re.DOTALL)
                if match:
                    result = json.loads(match.group(0))
                else:
                    result = {
                        "decision": "reject",
                        "reason": "No valid JSON detected from OPENAI output."
                    }

            except Exception as e:
                print(f"⚠️ openai/gpt-oss-20b API error: {e}")
                result = {"decision": "reject", "reason": str(e)}

    # 4️⃣ Save CEO decision back to memory.json
    project = project or {}
    project["ceo_decision"] = result.get("decision", "reject")
    project["ceo_reason"] = result.get("reason", "No valid reason provided.")
    project["status"] = (
        "Approved" if project["ceo_decision"] == "approve" else "Rejected"
    )

    data["current_project"] = project
    write_memory(data)

    print(f"✅ CEO Decision: {project['status']} — {project['ceo_reason']}")
    return {
        "status": "success",
        "decision": project["ceo_decision"],
        "reason": project["ceo_reason"],
        "project_title": project.get("project_title", "No project")
    }
