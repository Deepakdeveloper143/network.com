from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import socket
import ssl
import requests
import sys
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Add parent dir to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.supabase_client import get_supabase_client

router = APIRouter()

class PortScanRequest(BaseModel):
    target: str
    ports: Optional[List[int]] = [21, 22, 23, 25, 53, 80, 443, 3306, 5432, 8080, 8443]
    timeout: Optional[float] = 2.0

class WebsiteScanRequest(BaseModel):
    url: str

class VulnerabilityResponse(BaseModel):
    critical: int
    high: int
    medium: int
    low: int
    findings: List[Dict]
    severity_score: int

@router.post("/vulnerability-scan/port")
async def scan_ports(request: PortScanRequest):
    try:
        open_ports = []
        findings = []

        for port in request.ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(request.timeout)
            result = sock.connect_ex((request.target, port))
            sock.close()

            if result == 0:
                open_ports.append(port)
                service = get_service_name(port)
                severity = "medium"
                if port in [22, 3389]:
                    severity = "high"
                findings.append({
                    "port": port,
                    "service": service,
                    "severity": severity,
                    "description": f"Port {port} ({service}) is open"
                })

        critical = len([f for f in findings if f["severity"] == "critical"])
        high = len([f for f in findings if f["severity"] == "high"])
        medium = len([f for f in findings if f["severity"] == "medium"])
        low = len([f for f in findings if f["severity"] == "low"])
        severity_score = critical * 100 + high * 50 + medium * 25 + low * 10
        
        overall_severity = "Low"
        if critical > 0:
            overall_severity = "Critical"
        elif high > 0:
            overall_severity = "High"
        elif medium > 0:
            overall_severity = "Medium"

        response_data = VulnerabilityResponse(
            critical=critical,
            high=high,
            medium=medium,
            low=low,
            findings=findings,
            severity_score=min(severity_score, 100)
        )

        # Store in Supabase
        supabase = get_supabase_client()
        if supabase:
            try:
                supabase.table("scan_results").insert({
                    "scan_type": "vulnerability_port",
                    "scan_data": response_data.model_dump(),
                    "severity": overall_severity
                }).execute()
                
                # Update dashboard stats
                stats = supabase.table("dashboard_stats").select("*").order("recorded_at", desc=True).limit(1).execute()
                if stats.data:
                    current = stats.data[0]
                    new_vulns = current["vulnerabilities_found"] + len(findings)
                    new_threats = current["active_threats"] + (high + critical)
                    supabase.table("dashboard_stats").insert({
                        "total_scans": current["total_scans"] + 1,
                        "quantum_risk_score": current["quantum_risk_score"],
                        "active_threats": new_threats,
                        "prompt_attacks_blocked": current["prompt_attacks_blocked"],
                        "vulnerabilities_found": new_vulns,
                        "compliance_score": current["compliance_score"]
                    }).execute()
            except Exception as db_error:
                print(f"Warning: Could not store in database: {db_error}")

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scanning ports: {str(e)}")

@router.post("/vulnerability-scan/website")
async def scan_website(request: WebsiteScanRequest):
    try:
        findings = []
        url = request.url

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        # Check security headers
        try:
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers

            security_headers = {
                "X-Frame-Options": "Missing clickjacking protection",
                "X-XSS-Protection": "Missing XSS protection",
                "X-Content-Type-Options": "Missing MIME type sniffing protection",
                "Strict-Transport-Security": "Missing HSTS",
                "Content-Security-Policy": "Missing CSP",
                "Referrer-Policy": "Missing referrer policy",
                "Permissions-Policy": "Missing permissions policy"
            }

            for header, description in security_headers.items():
                if header not in headers:
                    findings.append({
                        "type": "Security Header",
                        "severity": "medium",
                        "description": f"{description}: {header}"
                    })

            # Check SSL certificate
            if url.startswith("https://"):
                try:
                    hostname = url.replace("https://", "").split("/")[0]
                    context = ssl.create_default_context()
                    with socket.create_connection((hostname, 443), timeout=5) as sock:
                        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                            cert = secure_sock.getpeercert()
                            if cert:
                                findings.append({
                                    "type": "SSL Certificate",
                                    "severity": "low",
                                    "description": "Valid SSL certificate detected"
                                })
                except ssl.SSLError:
                    findings.append({
                        "type": "SSL Certificate",
                        "severity": "high",
                        "description": "SSL certificate error detected"
                    })

        except Exception as e:
            findings.append({
                "type": "Connection",
                "severity": "medium",
                "description": f"Could not connect to {url}: {str(e)}"
            })

        critical = len([f for f in findings if f["severity"] == "critical"])
        high = len([f for f in findings if f["severity"] == "high"])
        medium = len([f for f in findings if f["severity"] == "medium"])
        low = len([f for f in findings if f["severity"] == "low"])
        severity_score = critical * 100 + high * 50 + medium * 25 + low * 10
        
        overall_severity = "Low"
        if critical > 0:
            overall_severity = "Critical"
        elif high > 0:
            overall_severity = "High"
        elif medium > 0:
            overall_severity = "Medium"

        response_data = VulnerabilityResponse(
            critical=critical,
            high=high,
            medium=medium,
            low=low,
            findings=findings,
            severity_score=min(severity_score, 100)
        )

        # Store in Supabase
        supabase = get_supabase_client()
        if supabase:
            try:
                supabase.table("scan_results").insert({
                    "scan_type": "vulnerability_website",
                    "scan_data": response_data.model_dump(),
                    "severity": overall_severity
                }).execute()
                
                # Update dashboard stats
                stats = supabase.table("dashboard_stats").select("*").order("recorded_at", desc=True).limit(1).execute()
                if stats.data:
                    current = stats.data[0]
                    new_vulns = current["vulnerabilities_found"] + len(findings)
                    new_threats = current["active_threats"] + (high + critical)
                    supabase.table("dashboard_stats").insert({
                        "total_scans": current["total_scans"] + 1,
                        "quantum_risk_score": current["quantum_risk_score"],
                        "active_threats": new_threats,
                        "prompt_attacks_blocked": current["prompt_attacks_blocked"],
                        "vulnerabilities_found": new_vulns,
                        "compliance_score": current["compliance_score"]
                    }).execute()
            except Exception as db_error:
                print(f"Warning: Could not store in database: {db_error}")

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scanning website: {str(e)}")

def get_service_name(port):
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        443: "HTTPS",
        3306: "MySQL",
        5432: "PostgreSQL",
        8080: "HTTP Proxy",
        8443: "HTTPS Alternate",
        3389: "RDP"
    }
    return services.get(port, "Unknown")
