# Implementation Guide

## Step-by-Step Deployment

### Phase 1: Physical Setup (Day 1)
1. Install core router (Cisco 2911)
2. Install core switch (Cisco 2960)
3. Connect fiber/copper uplinks
4. Label all cables

### Phase 2: Core Configuration (Day 2)
1. Configure core router (see `configs/core-router.txt`)
2. Set up VLAN interfaces
3. Configure DHCP pools
4. Test inter-VLAN routing

### Phase 3: Access Layer (Day 3)
1. Configure Floor 1 switch
2. Configure Floor 2 switch
3. Configure Floor 3 switch
4. Test port security

### Phase 4: Security Hardening (Day 4)
1. Apply ACLs
2. Enable port security
3. Configure NAT
4. Test firewall rules

### Phase 5: Validation (Day 5)
1. Run `python scripts/network_monitor.py`
2. Verify all devices online
3. Test internet connectivity per VLAN
4. Document any issues

## Troubleshooting Commands

```bash
# Check interface status
show ip interface brief

# Check VLANs
show vlan brief

# Check port security
show port-security

# Check routing
show ip route

# Check NAT
show ip nat translations

# Check DHCP
show ip dhcp pool
show ip dhcp binding

# Check ACLs
show access-lists
show ip interface GigabitEthernet0/1