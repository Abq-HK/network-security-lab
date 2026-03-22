#!/usr/bin/env python3
"""
Network Security Audit Tool
Checks for common security misconfigurations
"""

import json
from datetime import datetime


class SecurityAudit:
    def __init__(self):
        self.findings = []
        self.timestamp = datetime.now().isoformat()
    
    def check_vlan_segmentation(self, vlan_config):
        """Check if VLANs are properly segmented"""
        if len(vlan_config) < 3:
            self.findings.append({
                'severity': 'HIGH',
                'issue': 'Insufficient VLAN segmentation',
                'recommendation': 'Create separate VLANs for Admin, Teachers, Students'
            })
        else:
            self.findings.append({
                'severity': 'INFO',
                'issue': 'VLAN segmentation implemented',
                'status': 'PASS'
            })
    
    def check_port_security(self, switch_config):
        """Check if port security is enabled"""
        if 'port-security' in switch_config.lower():
            self.findings.append({
                'severity': 'INFO',
                'issue': 'Port security enabled',
                'status': 'PASS'
            })
        else:
            self.findings.append({
                'severity': 'HIGH',
                'issue': 'Port security not enabled',
                'recommendation': 'Enable port-security on all access ports'
            })
    
    def check_default_passwords(self, device_configs):
        """Check for default passwords"""
        default_passwords = ['admin', 'password', 'cisco', '1234']
        
        for config in device_configs:
            for pwd in default_passwords:
                if pwd in config.lower():
                    self.findings.append({
                        'severity': 'CRITICAL',
                        'issue': f'Default password detected: {pwd}',
                        'recommendation': 'Change all default passwords immediately'
                    })
    
    def generate_report(self):
        """Generate audit report"""
        report = {
            'audit_date': self.timestamp,
            'total_findings': len(self.findings),
            'critical': len([f for f in self.findings if f.get('severity') == 'CRITICAL']),
            'high': len([f for f in self.findings if f.get('severity') == 'HIGH']),
            'findings': self.findings
        }
        
        return report
    
    def print_report(self):
        """Print human-readable report"""
        report = self.generate_report()
        
        print("\n" + "=" * 50)
        print("NETWORK SECURITY AUDIT REPORT")
        print(f"Date: {report['audit_date']}")
        print("=" * 50)
        
        print(f"\nTotal Findings: {report['total_findings']}")
        print(f"Critical: {report['critical']}")
        print(f"High: {report['high']}")
        
        print("\n--- DETAILED FINDINGS ---")
        for i, finding in enumerate(self.findings, 1):
            severity = finding.get('severity', 'INFO')
            symbol = {'CRITICAL': '🔴', 'HIGH': '🟠', 'INFO': '🟢'}.get(severity, '⚪')
            
            print(f"\n{i}. {symbol} [{severity}] {finding.get('issue', 'N/A')}")
            
            if 'recommendation' in finding:
                print(f"   💡 Recommendation: {finding['recommendation']}")
            if 'status' in finding:
                print(f"   ✅ Status: {finding['status']}")
        
        print("\n" + "=" * 50)


# Demo
if __name__ == "__main__":
    audit = SecurityAudit()
    
    # Simulate checks
    sample_vlan = {'admin': 10, 'teachers': 20, 'students': 30}
    sample_config = "switchport port-security maximum 2"
    
    audit.check_vlan_segmentation(sample_vlan)
    audit.check_port_security(sample_config)
    
    # Generate and print report
    audit.print_report()
    
    # Save to file
    with open('security_audit_report.json', 'w') as f:
        json.dump(audit.generate_report(), f, indent=2)
    print("\n📄 Report saved to security_audit_report.json")