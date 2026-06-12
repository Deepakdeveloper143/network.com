# 🛡️ QuantumShieldAI - Quantum-Safe Security Platform

A comprehensive cybersecurity platform featuring quantum risk analysis, AI prompt protection, vulnerability scanning, and more!

## 🚀 Features

- **Quantum Risk Analyzer**: Analyze vulnerability to future quantum attacks
- **PromptPurify AI**: Protect LLMs from prompt injection and jailbreak attacks
- **Vulnerability Scanner**: Scan ports and websites for security issues
- **Quantum Vault (RSA)**: RSA encryption/decryption with quantum safety warnings
- **Signature Fraud Detection**: Detect forged digital signatures using AI
- **AI Security Copilot**: Chatbot for security guidance
- **Real-time Dashboard**: Complete security monitoring dashboard
- **Supabase Integration**: Persistent storage for scan results and dashboard data

## 📁 Project Structure

```
QuantumShieldAI/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI endpoints
│   │   ├── services/         # Business logic
│   │   ├── crewai_agents/    # CrewAI agents
│   │   ├── qiskit/           # Quantum computing integration
│   │   ├── scanner/          # Vulnerability scanner
│   │   ├── models/           # Database models
│   │   ├── reports/          # Report generation
│   │   ├── utils/            # Utilities
│   │   └── dashboard/        # Dashboard logic
│   ├── requirements.txt      # Backend dependencies
│   ├── .env                # Environment variables
│   └── supabase_schema.sql # Supabase database schema
├── frontend/
│   ├── app/
│   │   └── main.py           # Streamlit frontend
│   └── requirements.txt      # Frontend dependencies
├── landing page.html         # Landing page
├── start_backend.bat        # Windows: Start backend
└── start_frontend.bat       # Windows: Start frontend
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Groq API key (free at https://console.groq.com/)
- Supabase account (free at https://supabase.com/)

### Step 0: Configure Environment Variables

#### 0.1: Configure Groq API (Optional but Recommended)
1. Go to https://console.groq.com/ and create a free account
2. Generate an API key
3. Open `backend/.env` and replace `your_groq_api_key_here` with your actual Groq API key

#### 0.2: Configure Supabase (Optional but Recommended)
1. Go to https://supabase.com/ and create a free account
2. Create a new project
3. Go to Project Settings → API to get your:
   - Project URL
   - Service Role secret
4. Open the SQL Editor in Supabase
5. Copy and run the entire content of `backend/supabase_schema.sql` and execute it
6. Open `backend/.env` and update with your Supabase credentials:
   ```env
   GROQ_API_KEY=gsk_your_actual_key_here
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_SERVICE_KEY=your-service-role-key
   ```

### Step 1: Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the FastAPI server:
   ```bash
   python -m app.main
   ```
   The backend will be available at `http://localhost:8000`

6. Access API documentation:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Step 2: Frontend Setup

1. Open a new terminal window/tab

2. Install Streamlit:
   ```bash
   pip install streamlit requests plotly pillow
   ```

3. Navigate to the frontend directory:
   ```bash
   cd frontend/app
   ```

4. Start the Streamlit app:
   ```bash
   streamlit run main.py
   ```
   The frontend will be available at `http://localhost:8501`

### Step 3: Landing Page

Simply open `landing page.html` in your browser, or visit `http://localhost:8000`

## 🚀 Quick Start

1. Start the backend server first (port 8000)
2. Then start the frontend (port 8501)
3. Open your browser and navigate to `http://localhost:8501`

## 🌐 Deployment

### Backend on Render

1. Create a GitHub repo with your code
2. Sign up for a Render account
3. Create a new Web Service
4. Connect your GitHub repo
5. Configure:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `python -m backend.app.main`
6. Deploy!

### Frontend on Streamlit Community Cloud

1. Push your code to GitHub
2. Go to share.streamlit.io
3. Sign in and click "New app"
4. Select your repo, branch, and file path (`frontend/app/main.py`)
5. Deploy!

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/health` | GET | Health check |
| `/api/quantum-risk` | POST | Analyze quantum risk |
| `/api/prompt-analyze` | POST | Analyze prompt security |
| `/api/vulnerability-scan/port` | POST | Scan ports |
| `/api/vulnerability-scan/website` | POST | Scan website |
| `/api/rsa/generate-keys` | POST | Generate RSA keys |
| `/api/rsa/encrypt` | POST | Encrypt with RSA |
| `/api/rsa/decrypt` | POST | Decrypt with RSA |
| `/api/signature/check` | POST | Analyze signature |
| `/api/report/generate` | POST | Generate report |
| `/api/chatbot` | POST | Chat with security copilot |
| `/api/dashboard/stats` | GET | Get dashboard statistics |

## 🎨 Technologies Used

- **Backend**: FastAPI, Python
- **Frontend**: Streamlit, Plotly
- **Security**: Cryptography, SSL/TLS
- **Quantum**: Qiskit (for future enhancements)
- **AI**: CrewAI (agent framework), Groq API with Llama 3.1 8B Instant

## 📝 Notes

- This is a demonstration platform
- For production use, add proper authentication
- Replace placeholder AI/ML models with real implementations
- Add proper error handling and logging
- Configure secure database connections

## 📄 License

MIT License - feel free to use for learning and development!
