#!/usr/bin/env python3
"""
VLAN Configuration Generator
Automates Cisco switch configuration
"""

def generate_vlan_config(vlan_id, vlan_name, ports):
    """
    Generate Cisco IOS VLAN configuration
    
    Args:
        vlan_id: VLAN number (10, 20, 30, etc.)
        vlan_name: VLAN description
        ports: List of switch ports (e.g., ['Fa0/1', 'Fa0/2'])
    
    Returns:
        Configuration string for Cisco switch
    """
    config = []
    
    # Create VLAN
    config.append(f"vlan {vlan_id}")
    config.append(f" name {vlan_name}")
    config.append("!")
    
    # Configure access ports
    for port in ports:
        config.append(f"interface {port}")
        config.append(" switchport mode access")
        config.append(f" switchport access vlan {vlan_id}")
        config.append(" switchport port-security")
        config.append(" switchport port-security maximum 2")
        config.append(" switchport port-security violation restrict")
        config.append(" spanning-tree portfast")
        config.append("!")
    
    return "\n".join(config)


def generate_trunk_config(ports):
    """Generate trunk port configuration"""
    config = []
    
    for port in ports:
        config.append(f"interface {port}")
        config.append(" switchport mode trunk")
        config.append(" switchport trunk allowed vlan 10,20,30,99")
        config.append(" switchport trunk native vlan 99")
        config.append("!")
    
    return "\n".join(config)


# Generate configurations for each floor
if __name__ == "__main__":
    print("=" * 50)
    print("Cisco VLAN Configuration Generator")
    print("School Network - Kabul, Afghanistan")
    print("=" * 50)
    
    # Floor 1: Admin (VLAN 10)
    floor1_ports = ['Fa0/1', 'Fa0/2', 'Fa0/3', 'Fa0/4']
    print("\n--- FLOOR 1: ADMINISTRATION ---")
    print(generate_vlan_config(10, "ADMIN", floor1_ports))
    
    # Floor 2: Teachers (VLAN 20)
    floor2_ports = ['Fa0/5', 'Fa0/6', 'Fa0/7', 'Fa0/8']
    print("\n--- FLOOR 2: TEACHERS ---")
    print(generate_vlan_config(20, "TEACHERS", floor2_ports))
    
    # Floor 3: Students (VLAN 30)
    floor3_ports = ['Fa0/9', 'Fa0/10', 'Fa0/11', 'Fa0/12']
    print("\n--- FLOOR 3: STUDENTS ---")
    print(generate_vlan_config(30, "STUDENTS", floor3_ports))
    
    # Trunk ports (uplinks)
    trunk_ports = ['Gi0/1', 'Gi0/2']
    print("\n--- TRUNK PORTS ---")
    print(generate_trunk_config(trunk_ports))