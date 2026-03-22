#!/usr/bin/env python3
"""
Network Monitor - Real-time Network Health Check
Monitors: Ping, Bandwidth, Device Status
"""

import subprocess
import time
import json
from datetime import datetime


class NetworkMonitor:
    def __init__(self, config_file=None):
        self.devices = {
            'Core-Router': '192.168.1.1',
            'Floor1-Switch': '192.168.10.2',
            'Floor2-Switch': '192.168.20.2',
            'Floor3-Switch': '192.168.30.2',
            'Gateway': '8.8.8.8'
        }
        self.status_log = []
    
    def ping_device(self, ip, count=2):
        """Ping a device and return status"""
        try:
            result = subprocess.run(
                ['ping', '-n', str(count), '-w', '1000', ip],
                capture_output=True,
                text=True,
                timeout=3
            )
            success = result.returncode == 0
            
            # Parse time if success
            avg_time = None
            if success and 'Average' in result.stdout:
                try:
                    # Extract time from "Average = 1ms"
                    avg_line = [l for l in result.stdout.split('\n') if 'Average' in l][0]
                    avg_time = int(avg_line.split('Average = ')[1].split('ms')[0])
                except:
                    avg_time = 0
            
            return {
                'ip': ip,
                'status': 'UP' if success else 'DOWN',
                'latency_ms': avg_time,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'ip': ip,
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def check_all_devices(self):
        """Check all network devices"""
        print(f"\n{'='*60}")
        print(f"Network Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        results = {}
        for name, ip in self.devices.items():
            result = self.ping_device(ip)
            results[name] = result
            
            status_icon = '✅' if result['status'] == 'UP' else '❌'
            latency = f"{result['latency_ms']}ms" if result['latency_ms'] else 'N/A'
            
            print(f"{status_icon} {name:20} | {ip:15} | {result['status']:6} | {latency}")
        
        # Summary
        up_count = sum(1 for r in results.values() if r['status'] == 'UP')
        total = len(self.devices)
        
        print(f"{'='*60}")
        print(f"Summary: {up_count}/{total} devices online ({up_count/total*100:.0f}%)")
        print(f"{'='*60}")
        
        self.status_log.append({
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'summary': {'up': up_count, 'total': total}
        })
        
        return results
    
    def save_report(self, filename='network_report.json'):
        """Save monitoring report"""
        with open(filename, 'w') as f:
            json.dump(self.status_log, f, indent=2)
        print(f"\n📄 Report saved to {filename}")
    
    def continuous_monitor(self, interval=60):
        """Monitor continuously"""
        print("Starting continuous monitoring...")
        print(f"Interval: {interval} seconds")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.check_all_devices()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")
            self.save_report()


if __name__ == "__main__":
    monitor = NetworkMonitor()
    
    # Single check
    monitor.check_all_devices()
    
    # Save report
    monitor.save_report()
    
    # Or continuous (uncomment to use)
    # monitor.continuous_monitor(interval=60)