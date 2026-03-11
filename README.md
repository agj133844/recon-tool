#  Automated Network Reconnaissance Tool

![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

> A Python-based network reconnaissance tool designed for Phase 1 of authorized penetration testing engagements.

## Overview

This tool automates the initial reconnaissance phase of a penetration test by:
- Scanning target hosts/networks for open ports
- Detecting running services and version numbers
- Generating structured HTML and JSON reports for documentation

Built to mirror real-world pen testing workflows used in professional engagements.

## Features

- **3 scan modes**: Basic (top 1000 ports), Full (all ports + OS detection), Stealth (SYN scan)
- **Automatic reporting**: Generates timestamped HTML and JSON reports
- **Command-line interface**: Clean CLI for scripting into larger workflows
- **Structured output**: JSON output enables integration with SIEMs and other tools

## Installation
```bash
git clone https://github.com/YOUR_USERNAME/recon-tool.git
cd recon-tool
pip3 install -r requirements.txt
```

Prerequisites: Python 3.8+, Nmap

## Usage
```bash
# Basic scan (top 1000 ports)
python3 recon.py 192.168.1.1

# Full scan (all ports, OS detection)
python3 recon.py 192.168.1.1 --type full

# Stealth SYN scan
python3 recon.py 192.168.1.0/24 --type stealth
```

## Sample Output

![Sample Output](screenshot.png)

## Legal Disclaimer

This tool is intended strictly for authorized penetration testing and security research.
Only use against systems you own or have explicit written permission to test.
Unauthorized scanning may violate the Computer Fraud and Abuse Act (CFAA) and similar laws.

## Roadmap

- [ ] CVE lookup integration (via NVD API)
- [ ] Shodan API integration for external recon
- [ ] Slack/email alerting for automated scans
- [ ] Web dashboard for report viewing

## License

MIT License
