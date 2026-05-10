"""
Nexus Vanguard V6.0 — Scanner Engine with Vulnerability Analysis
"""
import concurrent.futures
import socket
import time
from typing import Callable, Dict, List, Optional

# ── Port Database ──────────────────────────────────────────────
KNOWN_PORTS: Dict[int, str] = {
    20:"FTP-DATA", 21:"FTP", 22:"SSH", 23:"Telnet", 25:"SMTP",
    53:"DNS", 67:"DHCP", 79:"Finger", 80:"HTTP", 88:"Kerberos",
    110:"POP3", 111:"RPCBind", 119:"NNTP", 123:"NTP", 135:"MSRPC",
    137:"NetBIOS-NS", 139:"NetBIOS-SSN", 143:"IMAP", 161:"SNMP",
    179:"BGP", 389:"LDAP", 443:"HTTPS", 445:"SMB", 465:"SMTPS",
    500:"IKE-VPN", 514:"Syslog", 587:"SMTP-Sub", 636:"LDAPS",
    873:"Rsync", 993:"IMAPS", 995:"POP3S", 1080:"SOCKS",
    1194:"OpenVPN", 1433:"MSSQL", 1521:"Oracle", 1723:"PPTP",
    1883:"MQTT", 2049:"NFS", 2375:"Docker-Unencrypted",
    2376:"Docker-TLS", 3000:"Grafana", 3306:"MySQL", 3389:"RDP",
    4369:"Erlang-EPM", 5000:"Flask-Dev", 5432:"PostgreSQL",
    5672:"RabbitMQ", 5900:"VNC", 5984:"CouchDB", 6379:"Redis",
    6443:"K8s-API", 7001:"WebLogic", 8000:"HTTP-Alt",
    8080:"Tomcat", 8443:"HTTPS-Alt", 8888:"Jupyter",
    9000:"SonarQube", 9090:"Prometheus", 9200:"Elasticsearch",
    9300:"ES-Cluster", 10250:"K8s-Kubelet", 11211:"Memcached",
    15672:"RabbitMQ-UI", 27017:"MongoDB", 27018:"MongoDB-Shard",
    50000:"SAP-Jenkins", 50070:"Hadoop-HDFS",
}

# ── Vulnerability Database (25 CVEs) ──────────────────────────
VULN_DB: Dict[str, Dict] = {
    "vsftpd 2.3.4":         {"cve":"CVE-2011-2523","severity":"CRITICAL","desc":"Backdoor command execution via smiley-face trigger"},
    "vsftpd 2.3.2":         {"cve":"CVE-2011-2523","severity":"HIGH",    "desc":"FTP backdoor variant"},
    "proftpd 1.3.3":        {"cve":"CVE-2010-4221","severity":"CRITICAL","desc":"Telnet IAC handling heap overflow"},
    "proftpd 1.3.5":        {"cve":"CVE-2015-3306","severity":"CRITICAL","desc":"Arbitrary file copy via SITE CPFR/CPTO"},
    "openssh 4.7":          {"cve":"CVE-2008-5161","severity":"HIGH",    "desc":"CBC-mode plaintext recovery attack"},
    "openssh 7.2":          {"cve":"CVE-2016-6515","severity":"HIGH",    "desc":"DoS via crafted auth packets (unbounded loop)"},
    "openssh 7.7":          {"cve":"CVE-2018-15473","severity":"MEDIUM", "desc":"Username enumeration via timing difference"},
    "apache 2.4.49":        {"cve":"CVE-2021-41773","severity":"CRITICAL","desc":"Path traversal & RCE (Actively exploited)"},
    "apache 2.4.50":        {"cve":"CVE-2021-42013","severity":"CRITICAL","desc":"Path traversal RCE bypass for 41773 patch"},
    "apache 2.2.3":         {"cve":"CVE-2007-5000","severity":"HIGH",    "desc":"Cross-site scripting in mod_status"},
    "nginx 1.16.1":         {"cve":"CVE-2021-23017","severity":"HIGH",   "desc":"Off-by-one heap overflow in DNS resolver"},
    "nginx 1.6.2":          {"cve":"CVE-2014-3616","severity":"MEDIUM",  "desc":"SSL session fixation via reuse"},
    "openssl 1.0.1":        {"cve":"CVE-2014-0160","severity":"CRITICAL","desc":"Heartbleed — private key and memory leak"},
    "openssl 1.0.2":        {"cve":"CVE-2016-2107","severity":"HIGH",    "desc":"Padding oracle MITM (DROWN variant)"},
    "openssl 1.1.0":        {"cve":"CVE-2017-3737","severity":"HIGH",    "desc":"Read/write after SSL_read error state"},
    "microsoft iis 6.0":    {"cve":"CVE-2017-7269","severity":"CRITICAL","desc":"WebDAV buffer overflow — Remote Code Execution"},
    "microsoft iis 5.0":    {"cve":"CVE-2001-0507","severity":"CRITICAL","desc":"Printer ISAPI extension overflow RCE"},
    "samba 3.5":            {"cve":"CVE-2017-7494","severity":"CRITICAL","desc":"EternalRed — arbitrary shared library loading RCE"},
    "exim 4.87":            {"cve":"CVE-2019-15846","severity":"CRITICAL","desc":"Heap buffer overflow via SNI in TLS negotiation"},
    "exim 4.92":            {"cve":"CVE-2019-10149","severity":"CRITICAL","desc":"Remote command execution via MAIL FROM"},
    "opensmtpd 6.6":        {"cve":"CVE-2020-7247","severity":"CRITICAL","desc":"Local/remote code execution as root"},
    "apache tomcat 9.0.0":  {"cve":"CVE-2020-1938","severity":"CRITICAL","desc":"Ghostcat — AJP arbitrary file read/include"},
    "apache tomcat 7.0":    {"cve":"CVE-2017-12617","severity":"CRITICAL","desc":"JSP file upload bypass — Remote Code Execution"},
    "redis 4.0":            {"cve":"CVE-2022-0543","severity":"CRITICAL","desc":"Lua sandbox escape — Remote Code Execution"},
    "php 5.6":              {"cve":"CVE-2019-11043","severity":"CRITICAL","desc":"FPM path_info underflow — Remote Code Execution"},
}

# ── Risk Classification ───────────────────────────────────────
HIGH_RISK  = {21,23,135,139,445,1433,2375,3389,5900,6379,9200,27017}
MED_RISK   = {22,25,53,80,443,110,143,3306,5432,8080,8888,50070}
HTTP_PORTS = {80,443,8000,8008,8080,8443,8888}
TIMEOUT    = 0.5


def analyze_vulnerability(banner: str) -> Optional[Dict]:
    b = banner.lower()
    for pattern, vuln in VULN_DB.items():
        if pattern in b:
            return vuln
    return None


def _base_risk(port: int) -> str:
    if port in HIGH_RISK: return "HIGH"
    if port in MED_RISK:  return "MEDIUM"
    return "LOW"


def _grab_banner(sock: socket.socket, port: int) -> str:
    try:
        sock.settimeout(TIMEOUT)
        if port in HTTP_PORTS:
            sock.sendall(b"HEAD / HTTP/1.0\r\nHost: nexusvanguard\r\n\r\n")
        data = sock.recv(1024)
        if data:
            decoded = data.decode("utf-8", errors="ignore").strip()
            return decoded.splitlines()[0][:120]
    except Exception:
        pass
    return ""


def scan_port(ip: str, port: int) -> Optional[Dict]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            if s.connect_ex((ip, port)) != 0:
                return None
            service = KNOWN_PORTS.get(port, "Unknown")
            banner  = _grab_banner(s, port)
            vuln    = analyze_vulnerability(banner)
            risk    = vuln["severity"] if vuln else _base_risk(port)
            return {
                "port":     port,
                "service":  service,
                "banner":   banner or "—",
                "risk":     risk,
                "cve":      vuln["cve"]  if vuln else None,
                "cve_desc": vuln["desc"] if vuln else None,
            }
    except (OSError, socket.error):
        return None


def scan_range(
    ip: str,
    start: int,
    end: int,
    threads: int,
    on_progress: Callable,
    on_port: Callable,
    on_done: Callable,
    stop_flag: list,          # stop_flag[0] = True → abort
) -> None:
    ports   = range(start, end + 1)
    total   = len(ports)
    done    = 0
    t0      = time.monotonic()
    threads = min(threads, 100)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(scan_port, ip, p): p for p in ports}
        for fut in concurrent.futures.as_completed(futures):
            if stop_flag[0]:
                ex.shutdown(wait=False, cancel_futures=True)
                return
            result = None
            try:
                result = fut.result()
            except Exception:
                pass
            done += 1
            elapsed = time.monotonic() - t0
            speed   = int(done / elapsed) if elapsed > 0 else 0
            if result:
                on_port(result)
            on_progress(done, total, speed, round(elapsed, 1))

    on_done(round(time.monotonic() - t0, 2))
