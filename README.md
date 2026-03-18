# 🎓 MARK4K — AI-Powered Academic Assistant
**Built for the DigitalOcean Gradient™ AI Hackathon**

Mark4k is an intelligent assistant designed for students and researchers. It provides academic path advice, analyzes complex PDF documents (syllabi, assignments, textbooks), and generates complete project source code using the power of **DigitalOcean Gradient AI (Qwen3 32B)**.

---

## 📂 Project Hierarchy

The project follows a standard Flask factory pattern for scalability and security:

```text
mark4k/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Academic Dark-Gold UI Theme
│   │   └── js/
│   │       └── script.js     # Frontend logic & Smart ZIP/PDF handling
│   ├── templates/
│   │   ├── base.html         # Master layout
│   │   ├── chat.html         # Main Workspace (Chat/PDF/Code)
│   │   ├── login.html        # Authentication: Login
│   │   └── register.html     # Authentication: Register
│   ├── __init__.py           # App factory & Database initialization
│   ├── models.py             # SQLite User models (Flask-SQLAlchemy)
│   ├── routes.py             # Chat, PDF analysis, and File routes
│   └── utils.py              # AI API calls, PDF generation, & ZIP building
├── .env                      # API Keys & Secret configurations
├── requirements.txt          # Project dependencies
├── run.py                    # Entry point to launch the application
├── mark4K_previous.py        # [LEGACY] Includes SMTP Email Sending feature
└── README.md                 # Project documentation
```

---

## 📧 Feature Note: Email Functionality
The current modular application focuses on high-performance chat, PDF analysis, and secure project generation. 

**Note:** The feature allowing users to draft and send academic emails via SMTP (Gmail App Passwords) is available in the **`mark4K_previous.py`** file located in the root directory. Users wishing to use the email module should refer to that specific script.

---

## 🚀 Features

- **Smart UI:** Academic "Dark Mode" with deep navy and gold accents.
- **Project Advisor:** Multi-turn chat for academic guidance.
- **PDF Analyzer:** Upload documents to extract summaries and task requirements.
- **Smart Code Generation:** Automatically detects source code in responses and offers a **Download ZIP** button.
- **Report Generation:** Export any AI conversation as a branded **PDF Document**.
- **Secure Auth:** SQLite-backed user registration and login system.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.9+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create or edit the `.env` file in the root directory and add your credentials:
```env
SECRET_KEY=your_secret_flask_key
AGENT_URL=https://cjkgjyoo5oezhc77dzx2dmbx.agents.do-ai.run/api/v1/chat/completions
AGENT_KEY=your_digitalocean_agent_key
```

### 4. Run the Application
```bash
python run.py
```
The app will be available at `http://localhost:5000`.

---

## ⚡ Tech Stack
*   **Backend:** Flask, Flask-SQLAlchemy, Flask-Login
*   **AI Engine:** DigitalOcean Gradient AI Agent (Qwen3 32B)
*   **Document Handling:** `pypdf` (Extraction) & `fpdf2` (Generation)
*   **Database:** SQLite

---
*Created for the DigitalOcean Gradient AI Hackathon 2025.*