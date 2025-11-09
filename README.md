# ⚙️ Code Company (Beta)

> **Full-Stack AI Company Simulation** — Automating intelligent project creation from idea to code execution.

![Flask](https://img.shields.io/badge/Backend-Flask-blue?style=for-the-badge&logo=flask)
![React](https://img.shields.io/badge/Frontend-React-61DBFB?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python)
![Tailwind](https://img.shields.io/badge/UI-TailwindCSS-38B2AC?style=for-the-badge&logo=tailwindcss)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Lint](https://github.com/Dkydgp/code-company-full/actions/workflows/lint.yml/badge.svg)
![Pylint](https://github.com/Dkydgp/code-company-full/actions/workflows/pylint.yml/badge.svg)

---

## 🏗️ Overview

**Code Company** is a full-stack simulation of a virtual AI-driven company.  
It automatically discovers coding projects online, makes executive decisions (via AI roles), executes them autonomously, and displays the outcomes on a beautiful interactive frontend.

🧩 Components:
- **Flask Backend** → Runs the AI workflow (Technical Manager → CEO → Operations)
- **React Frontend** → Displays live projects, statuses, and generated Python code
- **AI Engine (DeepSeek via OpenRouter)** → Handles reasoning and code generation
- **Web Search (Serper.dev)** → Finds real coding challenges and ideas

---

## 🧠 Features

✅ Full AI pipeline — from discovery to final code output  
✅ Roles implemented: Technical Manager, CEO, Operations Manager  
✅ Dynamic project execution and data persistence  
✅ REST API-based backend (Flask)  
✅ Live React frontend with TailwindCSS & Framer Motion  
✅ Real-time project viewer with modal and code download  
✅ “Run Company” one-click automation  
✅ Highlights latest project and lists all project codes  

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
├── .github/
│ └── workflows/
│ ├── lint.yml
│ └── pylint.yml
│
├── .gitignore
└── README.md


---

## 🧪 Continuous Integration (CI/CD)

Code Company includes **automated code quality checks** via **GitHub Actions**.

### 🧰 Workflows
| Workflow | Purpose | Badge |
|-----------|----------|--------|
| **PEP8 Lint** | Validates code style using `flake8` | ![Lint](https://github.com/Dkydgp/code-company-full/actions/workflows/lint.yml/badge.svg) |
| **Pylint Quality** | Calculates Pylint score and uploads badge | ![Pylint](https://github.com/Dkydgp/code-company-full/actions/workflows/pylint.yml/badge.svg) |

---

### 🧾 Universal Pylint Code Quality Check

This workflow runs **Pylint** across your repo, uploads a score, and fails the CI if your code falls below the quality threshold.

#### ✅ Features:
- Evaluates all `.py` files  
- Generates `pylint_report.txt` and `pylint_score.json`  
- Commits the score JSON for public visibility  
- Enforces minimum score (default `8.0/10`)  
- Uploads artifacts and badges automatically  

#### 🧩 Example usage in another repo:
```yaml
jobs:
  quality_check:
    uses: Dkydgp/code-company-full/.github/workflows/pylint.yml@main
    with:
      min_score: "8.5"
