#!/usr/bin/env python3
"""
Network Scanner - Educational Tool
Scans local network for active hosts
For authorized networks only
"""

import subprocess
import socket
import ipaddress


def ping_sweep(network_cidr):
    """
    Simple ping sweep for local network
    
    Example: ping_sweep("192.168.1.0/24")
    """
    print(f"Starting ping sweep: {network_cidr}")
    print("-" * 40)
    
    network = ipaddress.ip_network(network_cidr, strict=False)
    active_hosts = []
    
    # فقط ۵ IP اول برای demo (سریع‌تر)
    hosts = list(network.hosts())[:5]
    
    for ip in hosts:
        ip_str = str(ip)
        try:
            # Windows ping
            result = subprocess.run(
                ['ping', '-n', '1', '-w', '1000', ip_str],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                print(f"[+] {ip_str} is ACTIVE")
                active_hosts.append(ip_str)
            else:
                print(f"[-] {ip_str} no response")
                
        except Exception as e:
            print(f"[!] Error scanning {ip_str}: {e}")
    
    print("-" * 40)
    print(f"Found {len(active_hosts)} active hosts")
    return active_hosts


def get_local_ip():
    """Get local machine IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


if __name__ == "__main__":
    # گرفتن IP local خودکار
    local_ip = get_local_ip()
    print(f"Your IP: {local_ip}")
    
    # ساخت network range
    ip_parts = local_ip.split('.')
    network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
    
    print(f"Scanning network: {network}\n")
    
    # اجرا
    active = ping_sweep(network)
    
    print(f"\nActive hosts: {active}")