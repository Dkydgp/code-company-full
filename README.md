# ⚙️ Code Company (Beta)

> **Full-Stack AI Company Simulation** — Automating intelligent project creation from idea to code execution.

![Flask](https://img.shields.io/badge/Backend-Flask-blue?style=for-the-badge&logo=flask)
![React](https://img.shields.io/badge/Frontend-React-61DBFB?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python)
![Tailwind](https://img.shields.io/badge/UI-TailwindCSS-38B2AC?style=for-the-badge&logo=tailwindcss)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Lint](https://github.com/Dkydgp/code-company-full/actions/workflows/lint.yml/badge.svg)
![Score](https://github.com/Dkydgp/code-company-full/actions/workflows/score.yml/badge.svg)

---

## 🏗️ Overview

**Code Company** is a full-stack simulation of a virtual AI-driven company.  
It automatically discovers coding projects online, makes executive decisions (via AI roles), executes them autonomously, and displays the outcomes on a beautiful interactive frontend.

🧩 Components:
- **Flask Backend** → Runs the AI workflow (Technical Manager → CEO → Operations).
- **React Frontend** → Displays live projects, statuses, and generated Python code.
- **AI Engine (DeepSeek via OpenRouter)** → Handles logical reasoning and project execution.
- **Web Search (Serper.dev)** → Used for real-time coding project discovery.

---

## 🧠 Features

✅ Full AI pipeline — from idea discovery to final code output  
✅ Roles implemented: Technical Manager, CEO, Operations Manager  
✅ Dynamic project execution and storage  
✅ Integrated REST API (Flask backend)  
✅ Interactive frontend dashboard (React + TailwindCSS + Framer Motion)  
✅ Live project viewer with code preview, modal, and download options  
✅ “Run Company” one-click workflow trigger  
✅ Shows latest project and all project codes dropdown

---

## 🧩 Project Structure

code-company-full/
│
├── code_company_backend/ # Flask backend
│ ├── app/
│ ├── run.py
│ ├── requirements.txt
│ └── ...
│
├── code-company-frontend/ # React frontend
│ ├── src/
│ ├── package.json
│ ├── tailwind.config.js
│ └── ...
│
├── .gitignore
└── README.md



🧠 How It Works
Workflow

Technical Manager searches coding ideas online.

CEO decides whether to approve or reject the project.

Operations Manager executes the project and generates Python code.

The system saves the output in JSON and updates the frontend dynamically.

The frontend displays project details, summaries, and code in a beautiful UI.

🎨 Frontend UI

Key UI elements:

Sidebar navigation with quick actions

“Latest Project” highlight section

“All Codes” dropdown list (for exploring past projects)

Animated project grid (Framer Motion)

Detailed modal with Summary, Code, and Conclusion

📸 Screenshots (placeholders)

Add screenshots later after deployment.

Dashboard	Project Details

	
🚀 Deployment

You can host the stack easily:

Backend: Render / Railway / Hugging Face Spaces

Frontend: Vercel / Netlify / GitHub Pages

Update CORS and API base URLs accordingly.

🧑‍💻 Author

👨‍💻 Dipak Kumar Yadav
Creator of Code Company (Beta)
📧 yadavdipakkr@gmail.com
