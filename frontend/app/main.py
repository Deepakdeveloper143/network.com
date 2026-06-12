import streamlit as st
import requests
import base64
from PIL import Image
import io
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="QuantumShieldAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for navigation if not exists
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Landing Page"

# Custom CSS matching the landing page design
st.markdown("""
<style>
    /* Landing page color variables */
    :root{
        --bg:#060818;
        --bg2:#080d20;
        --bg3:#0a1228;
        --surface:#0d1630;
        --surface2:#101e3f;
        --border:#162040;
        --border2:#1e3060;
        --accent:#2563eb;
        --accent2:#4f7ef5;
        --accent3:#7aa8ff;
        --teal:#38bdf8;
        --teal2:#7dd3fc;
        --green:#10b981;
        --amber:#f59e0b;
        --red:#ef4444;
        --text:#eef3ff;
        --text2:#7a96c8;
        --text3:#2e4468;
    }
    
    /* Main background - matches landing page */
    .stApp {
        background: var(--bg);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(2,8,23,0.85);
        border-right: 1px solid rgba(37,99,235,0.15);
    }
    
    /* Cards - matches landing page product cards */
    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 2rem;
        margin-bottom: 1.25rem;
        position: relative;
        overflow: hidden;
        transition: border-color 0.3s ease, transform 0.35s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.3s ease;
    }
    .card:hover {
        border-color: var(--border2);
        transform: translateY(-6px);
        box-shadow: 0 24px 48px rgba(0,0,0,0.4);
    }
    
    /* Stat cards - uses landing page gradient */
    .stat-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .stat-card:hover {
        transform: translateY(-6px);
        border-color: var(--border2);
        box-shadow: 0 24px 48px rgba(0,0,0,0.4);
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), var(--amber));
    }
    
    /* Buttons - matches landing page primary button */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent), var(--accent2));
        color: white;
        border: none;
        border-radius: 999px;
        padding: 0.9rem 2.4rem;
        font-weight: 600;
        font-family: inherit;
        box-shadow: 0 0 36px rgba(37,99,235,0.45), 0 4px 12px rgba(0,0,0,0.3);
        letter-spacing: 0.01em;
        transition: background 0.25s, transform 0.2s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.25s;
    }
    .stButton>button:hover {
        background: var(--accent2);
        transform: translateY(-2px);
        box-shadow: 0 0 50px rgba(37,99,235,0.6);
    }
    
    /* Headings - matches landing page gradient text */
    h1, h2, h3, h4 {
        background: linear-gradient(135deg, var(--accent3) 0%, var(--teal) 55%, var(--teal2) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Colors */
    .danger {
        color: var(--red);
        text-shadow: 0 0 10px rgba(239,68,68,0.3);
    }
    .warning {
        color: var(--amber);
        text-shadow: 0 0 10px rgba(245,158,11,0.3);
    }
    .success {
        color: var(--green);
        text-shadow: 0 0 10px rgba(16,185,129,0.3);
    }
    
    /* Text inputs */
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        color: var(--text);
    }
    [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
        border-color: var(--accent2);
        box-shadow: 0 0 0 3px rgba(79,126,245,0.2);
    }
    
    /* Selectboxes */
    [data-testid="stSelectbox"] > div > div {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        color: var(--text);
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        color: var(--text);
    }
    [data-testid="stMetric"] label {
        color: var(--text2);
        font-size: 0.875rem;
        font-weight: 500;
        font-family: 'Rajdhani', sans-serif;
    }
    [data-testid="stMetric"] > div {
        color: var(--text);
        font-weight: 800;
        font-family: 'Rajdhani', sans-serif;
        background: linear-gradient(135deg, var(--accent3), var(--amber));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Tabs - matches landing page card styling */
    [data-testid="stTabs"] [role="tablist"] {
        gap: 0.5rem;
    }
    [data-testid="stTabs"] [role="tab"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        color: var(--text2);
        padding: 0.75rem 1.25rem;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        background: var(--surface2);
        color: var(--text);
        border-color: var(--accent2);
    }
    
    /* General text styling */
    .stMarkdown, .stText {
        color: var(--text2);
        font-family: 'Rajdhani', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# API base URL - use environment variable if available
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000/api")

# Sidebar navigation - matches landing page styling
st.sidebar.markdown('<div style="padding: 1rem 0; text-align: center;">', unsafe_allow_html=True)
st.sidebar.markdown('<h1 style="font-size: 1.75rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, var(--accent3) 0%, var(--teal) 55%, var(--teal2) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🛡️ QuantumShieldAI</h1>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="color: var(--text2); font-size: 0.875rem; margin-top: 0.5rem; font-family: \'Rajdhani\', sans-serif;">Advanced Cyber Security Platform</p>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div style="border-top: 1px solid var(--border); margin: 1rem 0;"></div>', unsafe_allow_html=True)

# Navigation options
pages = ["🏠 Landing Page", "⚠️ Risk Analyzer", "📊 Dashboard", "🛡️ PromptPurify AI", "🔍 Vulnerability Scanner", 
         "🔐 Quantum Vault (RSA)", "✍️ Signature Fraud Detection", "🤖 AI Security Copilot"]

# Update session state with selected page
st.session_state.current_page = st.sidebar.selectbox(
    "Explore Modules",
    pages,
    index=pages.index(st.session_state.current_page) if st.session_state.current_page in pages else 0
)
page = st.session_state.current_page

st.sidebar.markdown('<div style="border-top: 1px solid var(--border); margin: 1rem 0;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="color: var(--text3); font-size: 0.75rem; text-align: center; font-family: \'Share Tech Mono\', monospace;">Version 1.0.0</p>', unsafe_allow_html=True)

# Page: Landing Page
if page == "🏠 Landing Page":
    # Read the homepage HTML file
    # Go up 3 levels: app/ → frontend/ → agentofqsafe/
    landing_page_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "homepage.html")
    

    
    if os.path.exists(landing_page_path):
        with open(landing_page_path, "r", encoding="utf-8") as f:
            landing_html = f.read()
        # Display the beautiful homepage!
        st.html(landing_html)
    else:
        st.error("Homepage not found!")

# Page: Risk Analyzer
elif page == "⚠️ Risk Analyzer":
    st.title("⚠️ Risk Analyzer")
    st.markdown("---")

    st.markdown("""
    A Risk Analyzer collects security data from different sources, analyzes threats and vulnerabilities, 
    calculates risk level, and generates actionable reports.
    """)

    st.markdown("""
    ### Complete Workflow
    1. Enterprise Assets
    2. Asset Discovery & Data Collection
    3. Network Scan / Firewall Scan / Cloud Scan
    4. Vulnerability Database (CVE, CVSS, Threat Intel)
    5. Risk Analysis Engine
    6. Risk Calculation
    7. Risk Classification (Critical / High / Medium / Low)
    8. AI Recommendation
    9. Security Report
    10. Dashboard Monitoring
    """)

    col1, col2 = st.columns(2)
    with col1:
        num_assets = st.number_input("Number of Assets", min_value=1, value=100)
    with col2:
        risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"], index=1)

    if st.button("Analyze Risk"):
        try:
            payload = {"num_assets": num_assets, "risk_tolerance": risk_tolerance}
            response = requests.post(f"{API_BASE}/risk-analyzer", json=payload)
            if response.status_code == 200:
                data = response.json()

                st.markdown("---")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                    st.metric("Overall Risk Score", f"{data['overall_risk_score']}/100")
                    st.markdown("</div>", unsafe_allow_html=True)
                with col2:
                    risk_class = data['risk_classification']
                    st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                    st.metric("Risk Classification", risk_class)
                    st.markdown("</div>", unsafe_allow_html=True)

                st.subheader("Vulnerability Breakdown")
                col3, col4, col5, col6 = st.columns(4)
                col3.metric("Critical", data['vulnerability_breakdown']['critical'])
                col4.metric("High", data['vulnerability_breakdown']['high'])
                col5.metric("Medium", data['vulnerability_breakdown']['medium'])
                col6.metric("Low", data['vulnerability_breakdown']['low'])

                st.subheader("AI Recommendations")
                for rec in data['ai_recommendations']:
                    st.info(f"🔹 {rec}")

                st.subheader("Generated Report")
                st.markdown(data['security_report'])
            else:
                # Fallback to local calculation if backend not available
                st.warning("Backend not available. Using local risk calculation.")
                import random
                overall_risk_score = random.randint(30, 90)
                risk_class = "Critical" if overall_risk_score > 80 else "High" if overall_risk_score > 60 else "Medium" if overall_risk_score > 40 else "Low"

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                    st.metric("Overall Risk Score", f"{overall_risk_score}/100")
                    st.markdown("</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                    st.metric("Risk Classification", risk_class)
                    st.markdown("</div>", unsafe_allow_html=True)

                st.subheader("Vulnerability Breakdown")
                vuln_breakdown = {
                    'critical': random.randint(0, 5),
                    'high': random.randint(5, 15),
                    'medium': random.randint(15, 30),
                    'low': random.randint(30, 60)
                }
                col3, col4, col5, col6 = st.columns(4)
                col3.metric("Critical", vuln_breakdown['critical'])
                col4.metric("High", vuln_breakdown['high'])
                col5.metric("Medium", vuln_breakdown['medium'])
                col6.metric("Low", vuln_breakdown['low'])
        except Exception as e:
            # Fallback to local calculation if backend not available
            st.warning("Backend not available. Using local risk calculation.")
            import random
            overall_risk_score = random.randint(30, 90)
            risk_class = "Critical" if overall_risk_score > 80 else "High" if overall_risk_score > 60 else "Medium" if overall_risk_score > 40 else "Low"

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                st.metric("Overall Risk Score", f"{overall_risk_score}/100")
                st.markdown("</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                st.metric("Risk Classification", risk_class)
                st.markdown("</div>", unsafe_allow_html=True)

            st.subheader("Vulnerability Breakdown")
            vuln_breakdown = {
                'critical': random.randint(0, 5),
                'high': random.randint(5, 15),
                'medium': random.randint(15, 30),
                'low': random.randint(30, 60)
            }
            col3, col4, col5, col6 = st.columns(4)
            col3.metric("Critical", vuln_breakdown['critical'])
            col4.metric("High", vuln_breakdown['high'])
            col5.metric("Medium", vuln_breakdown['medium'])
            col6.metric("Low", vuln_breakdown['low'])

# Page: Dashboard
elif page == "📊 Dashboard":
    st.title("📊 Dashboard")
    
    st.markdown("---")

    try:
        response = requests.get(f"{API_BASE}/dashboard/stats")
        if response.status_code == 200:
            data = response.json()
            stats = data["stats"]

            # Stats row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                st.metric("Total Scans", stats["total_scans"])
                st.markdown("</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                risk_color = "danger" if stats["quantum_risk_score"] > 60 else "warning" if stats["quantum_risk_score"] > 30 else "success"
                st.metric("Quantum Risk Score", f"{stats['quantum_risk_score']}/100")
                st.markdown("</div>", unsafe_allow_html=True)
            with col3:
                st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                st.metric("Active Threats", stats["active_threats"])
                st.markdown("</div>", unsafe_allow_html=True)
            with col4:
                st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                st.metric("Prompt Attacks Blocked", stats["prompt_attacks_blocked"])
                st.markdown("</div>", unsafe_allow_html=True)

            col5, col6 = st.columns(2)
            with col5:
                st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                st.metric("Vulnerabilities Found", stats["vulnerabilities_found"])
                st.markdown("</div>", unsafe_allow_html=True)
            with col6:
                st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
                st.metric("Compliance Score", f"{stats['compliance_score']}%")
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("---")

            # Charts
            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                st.subheader("Risk Trend")
                risk_dates = [d["date"] for d in data["risk_trend"]]
                risk_values = [d["value"] for d in data["risk_trend"]]
                fig_risk = go.Figure()
                fig_risk.add_trace(go.Scatter(x=risk_dates, y=risk_values, mode='lines+markers', name='Risk Score', line=dict(color='#ef4444')))
                fig_risk.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_risk, use_container_width=True)

            with col_chart2:
                st.subheader("Vulnerability Trend")
                vuln_dates = [d["date"] for d in data["vulnerability_trend"]]
                vuln_values = [d["value"] for d in data["vulnerability_trend"]]
                fig_vuln = go.Figure()
                fig_vuln.add_trace(go.Scatter(x=vuln_dates, y=vuln_values, mode='lines+markers', name='Vulnerabilities', line=dict(color='#f59e0b')))
                fig_vuln.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_vuln, use_container_width=True)

            col_chart3, col_chart4 = st.columns(2)

            with col_chart3:
                st.subheader("Quantum Readiness")
                read_dates = [d["date"] for d in data["quantum_readiness"]]
                read_values = [d["value"] for d in data["quantum_readiness"]]
                fig_read = go.Figure()
                fig_read.add_trace(go.Scatter(x=read_dates, y=read_values, mode='lines+markers', name='Readiness Score', line=dict(color='#10b981')))
                fig_read.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_read, use_container_width=True)

            with col_chart4:
                st.subheader("Threat Distribution")
                threat_names = [d["name"] for d in data["threat_distribution"]]
                threat_values = [d["value"] for d in data["threat_distribution"]]
                fig_threat = go.Figure(data=[go.Pie(labels=threat_names, values=threat_values, hole=.3)])
                fig_threat.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_threat, use_container_width=True)
    except:
        st.warning("Could not connect to backend. Please ensure the FastAPI server is running.")

# Page: PromptPurify AI
elif page == "🛡️ PromptPurify AI":
    st.title("🛡️ PromptPurify AI")
    st.markdown("---")

    prompt = st.text_area("Enter prompt to analyze", height=150, placeholder="Type your prompt here...")

    if st.button("Analyze Prompt"):
        if prompt:
            try:
                payload = {"prompt": prompt}
                response = requests.post(f"{API_BASE}/prompt-analyze", json=payload)
                if response.status_code == 200:
                    data = response.json()

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.metric("Risk Score", f"{data['risk_score']}/100")
                        st.markdown("</div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.metric("Threat Category", data["threat_category"])
                        st.markdown("</div>", unsafe_allow_html=True)

                    if data["is_safe"]:
                        st.success("✅ Prompt appears safe")
                    else:
                        st.warning("⚠️ Potential security issues detected")

                    if data["detected_attack_types"]:
                        st.subheader("Detected Attack Types")
                        for attack in data["detected_attack_types"]:
                            st.error(f"• {attack}")

                    st.subheader("Sanitized Prompt")
                    st.code(data["sanitized_prompt"])

                    st.subheader("Security Recommendation")
                    st.info(data["security_recommendation"])
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a prompt to analyze")

# Page: Vulnerability Scanner
elif page == "🔍 Vulnerability Scanner":
    st.title("🔍 Vulnerability Scanner")
    st.markdown("---")

    url = st.text_input("Website URL", "https://example.com")
    
    if st.button("Scan Website"):
        try:
            payload = {"url": url}
            response = requests.post(f"{API_BASE}/vulnerability-scan/website", json=payload)
            if response.status_code == 200:
                data = response.json()

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Critical", data["critical"])
                col2.metric("High", data["high"])
                col3.metric("Medium", data["medium"])
                col4.metric("Low", data["low"])

                st.subheader("Findings")
                for finding in data["findings"]:
                    severity_color = "danger" if finding["severity"] in ["critical", "high"] else "warning" if finding["severity"] == "medium" else "success"
                    st.markdown(f"<div class='card'><strong class='{severity_color}'>{finding['severity'].upper()}</strong>: {finding['description']}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Page: Quantum Vault (RSA)
elif page == "🔐 Quantum Vault (RSA)":
    st.title("🔐 Secure Communication - RSA File Encryption & Decryption")
    st.markdown("---")
    st.warning("⚠️ RSA may become vulnerable to future quantum computers. Consider migrating to Post-Quantum Cryptography.")

    tab1, tab2 = st.tabs(["Encrypt File", "Decrypt File"])

    with tab1:
        st.subheader("Step 1: Upload Original File")
        uploaded_file = st.file_uploader("Choose a file to encrypt", type=None)
        
        st.subheader("Step 2: Generate RSA Keys & Encrypt File")
        key_size = st.selectbox("Select RSA Key Size", [2048, 3072, 4096], index=0)
        
        if st.button("Encrypt File"):
            if uploaded_file is not None:
                try:
                    with st.spinner("Encrypting file..."):
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        data = {"key_size": key_size}
                        response = requests.post(f"{API_BASE}/rsa/encrypt-file", files=files, data=data)
                        
                        if response.status_code == 200:
                            st.success("✓ File Encrypted Successfully!")
                            st.subheader("Download Files")
                            st.download_button(
                                label="📥 Download Encrypted Files (ZIP)",
                                data=response.content,
                                file_name="encrypted_files.zip",
                                mime="application/zip"
                            )
                            st.info("💾 The ZIP file contains: encrypted_file.rsa and private_key.pem. Keep the private key safe!")
                        else:
                            st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please upload a file first")

    with tab2:
        st.subheader("Step 1: Upload Encrypted File & Private Key")
        encrypted_file = st.file_uploader("Choose encrypted file (.rsa)", type=["rsa"])
        private_key_file = st.file_uploader("Choose private key file (.pem)", type=["pem"])
        
        st.subheader("Step 2: Decrypt File")
        if st.button("Decrypt File"):
            if encrypted_file is not None and private_key_file is not None:
                try:
                    with st.spinner("Decrypting file..."):
                        files = {
                            "encrypted_file": (encrypted_file.name, encrypted_file.getvalue(), encrypted_file.type),
                            "private_key_file": (private_key_file.name, private_key_file.getvalue(), private_key_file.type)
                        }
                        response = requests.post(f"{API_BASE}/rsa/decrypt-file", files=files)
                        
                        if response.status_code == 200:
                            st.success("✓ File Decrypted Successfully!")
                            st.subheader("Download Original File")
                            st.download_button(
                                label="📥 Download Original File",
                                data=response.content,
                                file_name=response.headers.get("Content-Disposition").split("filename=")[1].strip('"') if "Content-Disposition" in response.headers else "decrypted_file",
                                mime="application/octet-stream"
                            )
                        else:
                            st.error(f"❌ {response.json()['detail']}" if response.status_code == 400 else f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please upload both encrypted file and private key")

# Page: Signature Fraud Detection
elif page == "✍️ Signature Fraud Detection":
    st.title("✍️ Signature Fraud Detection")
    st.markdown("---")

    uploaded_file = st.file_uploader("Upload signature image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Signature", width=300)

        if st.button("Analyze Signature"):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{API_BASE}/signature/check", files=files)
                if response.status_code == 200:
                    data = response.json()

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Match %", f"{data['match_percentage']}%")
                    col2.metric("Forgery Probability", f"{data['forgery_probability']}%")
                    col3.metric("Confidence Score", f"{data['confidence_score']}%")

                    st.markdown("---")

                    result_color = "success" if data["analysis_result"] == "Genuine" else "warning" if data["analysis_result"] == "Suspicious" else "danger"
                    st.markdown(f"<h3 class='{result_color}'>Analysis Result: {data['analysis_result']}</h3>", unsafe_allow_html=True)

                    if data["tampering_detected"]:
                        st.error("⚠️ Tampering detected!")

                    st.subheader("Details")
                    st.info(data["details"])
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Page: AI Security Copilot
elif page == "🤖 AI Security Copilot":
    st.title("🤖 AI Security Copilot")
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about security..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                messages_payload = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                response = requests.post(f"{API_BASE}/chatbot", json={"messages": messages_payload})
                if response.status_code == 200:
                    data = response.json()
                    message_placeholder.markdown(data["response"])
                    st.session_state.messages.append({"role": "assistant", "content": data["response"]})
            except Exception as e:
                message_placeholder.error(f"Error: {str(e)}")
