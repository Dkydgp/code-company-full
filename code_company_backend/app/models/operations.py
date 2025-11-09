import requests
import json
import re
from config import Config
from app.utils.json_handler import read_memory, write_memory


def execute_project():
    """
    ⚙️ Operations Manager — Executes the approved project.
    Generates working Python code, explanation, and summary using OpenRouter (free model).
    Handles malformed JSON gracefully and avoids parsing errors.
    """

    data = read_memory()
    project = data.get("current_project")

    # 1️⃣ Check if a project exists
    if not project:
        return {"status": "error", "message": "No project found. Run Technical Manager first."}

    # 2️⃣ Ensure CEO approved it
    if project.get("status") != "Approved":
        return {"status": "error", "message": "Project not approved by CEO yet."}

    title = project.get("project_title", "Unnamed Project")
    summary = project.get("problem_summary", "No summary available.")

    # 3️⃣ Create the AI prompt
    prompt = f"""
    You are the Operations Manager of Code Company (Beta).
    The CEO has approved the following project.

    🧩 Project Title: {title}
    🧠 Description: {summary}

    Your tasks:
    1. Write clean, efficient, working Python code that implements this project.
    2. Explain how your code works in detailed steps.
    3. Provide a final summary (purpose and expected outcome).

    Respond ONLY in valid JSON format:
    {{
        "solution_summary": "Brief summary of the solution",
        "detailed_steps": "Explain how the code works step by step",
        "final_code": "Full Python code here",
        "conclusion": "Final explanation of the project"
    }}
    """

    try:
        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://127.0.0.1:5000",
            "X-Title": "Code Company (Beta)"
        }

        payload = {
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a senior Python engineer and operations AI. "
                        "Respond ONLY in strict JSON format — no Markdown, no explanations outside JSON."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        }

        # 🛰️ Send request to OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=90
        )
        response.raise_for_status()

        ai_reply = response.json()["choices"][0]["message"]["content"].strip()

        # 🧩 Try extracting JSON portion even if AI adds extra text
        match = re.search(r"\{.*\}", ai_reply, re.DOTALL)

        if match:
            try:
                result = json.loads(match.group(0))
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON Decode Error: {e}")
                # Fallback to raw text mode if JSON invalid
                result = {
                    "solution_summary": "Partial AI response (invalid JSON).",
                    "detailed_steps": "",
                    "final_code": ai_reply,
                    "conclusion": "JSON parsing failed, raw AI text used instead."
                }
        else:
            # No JSON detected at all — store plain text safely
            result = {
                "solution_summary": "No valid JSON detected from AI output.",
                "detailed_steps": "",
                "final_code": ai_reply,
                "conclusion": "Raw text stored instead of structured output."
            }

    except Exception as e:
        print(f"⚠️ Operations Manager Error: {e}")
        return {"status": "error", "message": str(e)}

    # 4️⃣ Save the operation result to memory.json
    project["operations_result"] = result
    project["status"] = "Completed"
    data["current_project"] = project
    write_memory(data)

    print(f"✅ Operations Manager: Successfully executed project '{title}'")

    # 5️⃣ Return clean response for API
    return {
        "status": "success",
        "message": "Project executed successfully",
        "project_title": title,
        "solution_summary": result.get("solution_summary", "No summary provided."),
        "conclusion": result.get("conclusion", "No conclusion provided."),
        "final_code": result.get("final_code", "# No code provided.")
    }
