#!/usr/bin/env python3
"""
Automated Network Reconnaissance Tool
Author: [Your Name]
Description: Phase 1 recon tool for authorized penetration testing engagements.
             Performs port scanning, service detection, and generates HTML reports.
"""

import nmap
import argparse
import datetime
import json
import os

def run_scan(target, scan_type="basic"):
    """Run nmap scan against target."""
    nm = nmap.PortScanner()
    
    print(f"\n[*] Starting reconnaissance on: {target}")
    print(f"[*] Scan type: {scan_type}")
    print(f"[*] Time: {datetime.datetime.now()}\n")

    if scan_type == "basic":
        # Top 1000 ports, service version detection
        nm.scan(target, arguments="-sV --top-ports 1000")
    elif scan_type == "full":
        # All ports, OS detection, scripts
        nm.scan(target, arguments="-sV -sC -O -p-")
    elif scan_type == "stealth":
        # SYN scan, quieter
        nm.scan(target, arguments="-sS -sV --top-ports 100")

    return nm

def parse_results(nm, target):
    """Parse nmap results into structured data."""
    results = {
        "target": target,
        "scan_time": str(datetime.datetime.now()),
        "hosts": []
    }

    for host in nm.all_hosts():
        host_data = {
            "ip": host,
            "hostname": nm[host].hostname(),
            "state": nm[host].state(),
            "open_ports": []
        }

        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                port_info = nm[host][proto][port]
                if port_info["state"] == "open":
                    host_data["open_ports"].append({
                        "port": port,
                        "protocol": proto,
                        "service": port_info.get("name", "unknown"),
                        "version": port_info.get("version", ""),
                        "product": port_info.get("product", "")
                    })
                    print(f"  [+] {host}:{port}/{proto} - {port_info.get('name','?')} {port_info.get('product','')} {port_info.get('version','')}")

        results["hosts"].append(host_data)

    return results

def generate_html_report(results):
    """Generate a clean HTML report."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.html"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Recon Report - {results['target']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
        h1 {{ color: #00ff88; }}
        h2 {{ color: #00ccff; border-bottom: 1px solid #333; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th {{ background: #16213e; color: #00ff88; padding: 8px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid #333; }}
        .meta {{ color: #aaa; font-size: 0.9em; }}
        .open {{ color: #00ff88; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>🔍 Recon Report</h1>
    <p class="meta">Target: <strong>{results['target']}</strong> | Scan Time: {results['scan_time']}</p>
    <p><em>⚠️ Generated for authorized penetration testing only.</em></p>
"""

    for host in results["hosts"]:
        html += f"""
    <h2>Host: {host['ip']} {f"({host['hostname']})" if host['hostname'] else ""}</h2>
    <p>State: <span class="open">{host['state']}</span></p>
    <table>
        <tr><th>Port</th><th>Protocol</th><th>Service</th><th>Product</th><th>Version</th></tr>
"""
        for p in host["open_ports"]:
            html += f"""
        <tr>
            <td>{p['port']}</td>
            <td>{p['protocol']}</td>
            <td>{p['service']}</td>
            <td>{p['product']}</td>
            <td>{p['version']}</td>
        </tr>"""

        html += "</table>"

    html += """
</body>
</html>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    # Also save JSON
    json_file = f"report_{timestamp}.json"
    with open(json_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n[✓] HTML report saved: {filename}")
    print(f"[✓] JSON report saved: {json_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Recon Tool - Authorized penetration testing use only"
    )
    parser.add_argument("target", help="Target IP, range, or hostname (e.g. 192.168.1.1 or 192.168.1.0/24)")
    parser.add_argument("--type", choices=["basic", "full", "stealth"], default="basic",
                        help="Scan type (default: basic)")
    args = parser.parse_args()

    print("=" * 60)
    print("   RECON TOOL - FOR AUTHORIZED USE ONLY")
    print("=" * 60)

    nm = run_scan(args.target, args.type)
    results = parse_results(nm, args.target)
    generate_html_report(results)

if __name__ == "__main__":
    main()