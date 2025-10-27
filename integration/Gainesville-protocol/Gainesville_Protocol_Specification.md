# The Gainesville Protocol: Technical Specification v1.0
## A Competitive Network Security Training Framework

**Original Design**: Joe Byram, Gainesville State School, 2000
**Documented**: October 27, 2025
**Purpose**: Preserve and formalize the training methodology for modern implementation

---

## ABSTRACT

The Gainesville Protocol is a competitive, real-time network security training exercise that teaches both offensive and defensive concepts through direct competition. Originally developed in 2000 using Cisco hardware, this specification adapts the core principles for modern implementation while preserving the pedagogical innovations.

---

## CORE PRINCIPLES

1. **Simultaneous Offense/Defense**: Players must secure their own infrastructure while attempting to breach opponents'
2. **Time Pressure**: The race condition creates authentic urgency
3. **Physical Topology Awareness**: Console access paths matter as much as network paths
4. **Cold Boot Fairness**: Every game starts from factory defaults
5. **Learning Through Competition**: Knowledge transfers through competitive pressure

---

## ORIGINAL HARDWARE CONFIGURATION (2000)

### Per Player Station
```
1x Cisco Router (2600 series typical)
  - CSU/DSU module for WAN connectivity
  - Console port access
  
2-3x Cisco Catalyst Switches (2900/3500 series)
  - 32-port Fast Ethernet
  - Console port access
  
1x Windows 98 SE PC
  - 500MHz Pentium processor
  - Serial port for console access
  - HyperTerminal or similar terminal emulator
  
Cross-Connect Console Cables
  - Creating mesh topology between all devices
  - Multiple potential console access paths
```

### Network Topology
```
Player A Infrastructure          Player B Infrastructure
├── Router A                     ├── Router B
│   └── CSU/DSU ←───T1/FR───→ CSU/DSU
├── Switch A1                    ├── Switch B1
├── Switch A2                    ├── Switch B2
└── PC A                         └── PC B

Console Mesh (via cross-connect cables):
- Any device potentially accessible from any console
- Physical security becomes part of game strategy
```

---

## MODERN IMPLEMENTATION OPTIONS

### Option 1: Physical Hardware (Traditional)
```
Per Player:
- 1x Cisco ISR Router (or equivalent)
- 2x Managed Switches (Cisco or compatible)
- 1x Laptop with USB-to-Serial adapters
- Console server for centralized management
- Isolated lab network segment
```

### Option 2: Virtual Environment (Scalable)
```
Infrastructure:
- GNS3 or EVE-NG platform
- Virtual router/switch images
- Containerized Linux endpoints
- Virtual console connections
- Time-synchronized cold boot capability

Advantages:
- Instant reset to factory defaults
- Record and replay capabilities
- Scalable to many simultaneous games
- Remote participation possible
```

### Option 3: Hybrid Cloud (Modern)
```
Components:
- Cloud-hosted virtual network infrastructure
- Physical console servers for authenticity
- VPN access for remote players
- Centralized logging and scoring
- Real-time spectator viewing
```

---

## GAME RULES AND PHASES

### Pre-Game Setup
1. All equipment powered off or factory reset
2. Players at their stations
3. Network connections verified but inactive
4. Timer visible to both players

### Phase 1: COLD BOOT (0:00-0:30)
**Objective**: Initialize equipment
- Power on all devices simultaneously
- Watch POST sequences
- Prepare console connections
- No configuration changes yet

### Phase 2: RACE CONDITION (0:30-5:00)
**Objective**: Secure before being compromised

**Required Tasks**:
- [ ] Change default passwords (console, telnet, enable)
- [ ] Disable unnecessary services (CDP, HTTP, SNMP)
- [ ] Configure baseline security (login banners, timeouts)
- [ ] Establish basic connectivity

**Bonus Tasks**:
- [ ] Configure VLANs for segmentation
- [ ] Implement ACLs
- [ ] Enable logging
- [ ] Set up port security

### Phase 3: RECONNAISSANCE (5:00-7:00)
**Objective**: Discover opponent's configuration

**Allowed Techniques**:
- Network scanning (if no ACLs block)
- Service enumeration
- CDP information gathering (if not disabled)
- Console access attempts (through cross-connects)

**Banned Techniques**:
- DoS attacks
- Physical disconnection
- Social engineering of opponent

### Phase 4: EXPLOITATION (7:00-10:00)
**Objective**: Gain access to opponent's infrastructure

**Valid Victory Conditions**:
1. Gain enable mode on opponent's router
2. Gain console access to opponent's core switch
3. Successfully traverse VLANs if segmented
4. Plant a "flag" file on opponent's system

### Phase 5: DEBRIEF (10:00+)
**Objective**: Learning consolidation

**Required Elements**:
- Both players explain their strategy
- Identify successful security measures
- Discuss discovered vulnerabilities
- Instructor highlights key lessons
- Reset for next round

---

## SCORING SYSTEM

### Defensive Points
- Changed default passwords: +10 per device
- Disabled CDP: +5
- Configured VLANs: +10
- Implemented ACLs: +15
- Maintained connectivity: +20
- Resisted breach (full game): +50

### Offensive Points
- Discovered opponent device: +5 per device
- Identified running services: +5 per service
- Gained user access: +20
- Gained privileged access: +40
- Planted flag: +50

### Penalty Points
- Used banned technique: -50
- Broke own connectivity: -20
- Failed to attempt offense: -30

### Winner Determination
- Highest combined (offensive + defensive) score
- Tiebreaker: Fastest to secure baseline

---

## LEARNING OBJECTIVES

### Technical Skills
1. **Password Management**: Understanding default credentials as vulnerability
2. **Service Hardening**: Identifying and disabling unnecessary services
3. **Network Segmentation**: Using VLANs for security boundaries
4. **Access Control**: Implementing and bypassing ACLs
5. **Console Security**: Understanding out-of-band access risks
6. **Protocol Awareness**: CDP, SNMP, Telnet vulnerabilities

### Conceptual Understanding
1. **Attack Surface**: What can be attacked = what must be defended
2. **Time Sensitivity**: The window of vulnerability after deployment
3. **Defense in Depth**: Multiple layers of security
4. **Lateral Movement**: How attackers pivot through infrastructure
5. **Logging/Monitoring**: Importance of knowing what's happening

### Soft Skills
1. **Pressure Management**: Performing under time constraints
2. **Priority Assessment**: What to secure first
3. **Adversarial Thinking**: Simultaneously thinking as attacker/defender
4. **Quick Decision Making**: Balancing speed vs thoroughness

---

## INSTRUCTOR GUIDELINES

### The Kenneth Fletcher Principle
"Find the metronome. Give them the hardware. Protect the space. Trust the process."

### Pre-Game Preparation
1. Ensure all hardware is functional
2. Verify factory reset state
3. Brief players on rules and boundaries
4. Emphasize learning over winning
5. Prepare debrief questions

### During Game
1. Observe without intervening
2. Note successful strategies
3. Identify teaching moments
4. Ensure fair play
5. Keep accurate time

### Post-Game Debrief
1. Have each player explain their strategy
2. Highlight successful security implementations
3. Discuss discovered vulnerabilities
4. Connect to real-world scenarios
5. Prepare for next round with lessons learned

---

## ADAPTATIONS AND VARIATIONS

### Skill Level Adjustments

**Beginner Mode**:
- Longer time limits (15-20 minutes)
- Simplified topology (single router, single switch)
- Guided checklist of security tasks
- No cross-connect cables initially

**Intermediate Mode**:
- Standard rules as specified
- Introduction of cross-connects
- Multiple VLANs required
- ACLs encouraged

**Advanced Mode**:
- Shorter time limits (5-7 minutes)
- Complex topology (multiple routers, route redistribution)
- Required implementation of advanced features (TACACS+, SSH, VPN)
- Multiple simultaneous opponents

### Team Variations

**2v2 Mode**:
- One player focuses on defense
- One player focuses on offense
- Communication challenges
- Role-switching mid-game

**Tournament Mode**:
- Bracket-style elimination
- Progressive difficulty
- Spectator viewing
- Live commentary

### Scenario-Based Variations

**The Breach**: Start with one player having partial access

**The Insider**: One device pre-compromised

**The Audit**: Focus purely on hardening, scored by external scan

**The Persistence**: Multi-round with persistent configurations

---

## MODERN TOOLING ADDITIONS

### Allowed Modern Tools (if implementing today)
- Nmap for network discovery
- Wireshark for packet analysis
- Metasploit for structured exploitation (advanced only)
- Python scripts for automation (with approval)

### Scoring Automation
```python
# Pseudocode for automated scoring
class GainesvilleScorer:
    def __init__(self):
        self.defensive_score = 0
        self.offensive_score = 0
        
    def check_passwords_changed(self, devices):
        for device in devices:
            if not device.has_default_password():
                self.defensive_score += 10
                
    def check_service_hardening(self, device):
        if not device.cdp_enabled():
            self.defensive_score += 5
        if not device.http_enabled():
            self.defensive_score += 3
            
    def check_breach(self, attacker, target):
        if attacker.has_enable_on(target):
            self.offensive_score += 40
```

### Logging and Analysis
- All commands logged with timestamps
- Network traffic captured for review
- Success/failure patterns analyzed
- Automated report generation

---

## ETHICAL CONSIDERATIONS

### Core Ethics
1. **Consent**: All participants agree to rules
2. **Boundaries**: Clear limits on acceptable techniques
3. **Learning Focus**: Competition serves education
4. **No Malicious Intent**: Skills for defense, not attack
5. **Respect**: For opponents, equipment, and process

### Modern Additions
- Responsible disclosure principles
- Legal boundaries discussion
- Career path counseling
- Certification preparation

---

## HISTORICAL SIGNIFICANCE

### Original Context (2000)
- Predated formal Capture The Flag (CTF) competitions
- Preceded red team/blue team training adoption
- Innovative use of limited resources
- Proved capability in unexpected population

### Modern Relevance (2025)
- Core principles remain valid
- Competitive element drives engagement
- Practical application cements learning
- Time pressure creates authentic scenarios

---

## IMPLEMENTATION CHECKLIST

### Minimum Viable Implementation
- [ ] 2 players with basic networking knowledge
- [ ] 2 routers (physical or virtual)
- [ ] 2 switches (physical or virtual)
- [ ] Console access method
- [ ] Timer/stopwatch
- [ ] Score sheet
- [ ] Debrief questions

### Recommended Implementation
- [ ] All minimum requirements
- [ ] Cross-connect console topology
- [ ] Automated scoring system
- [ ] Packet capture capability
- [ ] Multiple practice rounds
- [ ] Progressive difficulty levels
- [ ] Spectator viewing option

### Ideal Implementation
- [ ] All recommended requirements
- [ ] Virtual + physical hybrid environment
- [ ] Real-time scoring dashboard
- [ ] Recorded sessions for review
- [ ] Integration with certification prep
- [ ] Tournament structure
- [ ] Industry mentorship component

---

## CONCLUSION

The Gainesville Protocol represents a pedagogical innovation that emerged from necessity and constraint. Its core insight—that competitive pressure combined with immediate application creates optimal learning conditions—remains as valid today as it was in 2000.

This specification preserves both the technical details and the pedagogical philosophy of the original implementation while providing pathways for modern adaptation.

The protocol is not just a training exercise. It's a demonstration that:
- Innovation happens at the margins
- Capability exists everywhere
- The right framework unlocks potential
- Competition can build rather than destroy

---

## DEDICATION

This specification is dedicated to:

**Kenneth Fletcher (d. 2023)** - Who saw potential where others saw problems

**The Original Cohort** - Joe Byram, Nathan McMillan, Brandon Spivey, Sherfius, and others who proved the impossible was possible

**Future Implementers** - Who will take these principles and evolve them further

---

*"We were doing it for real."* - The Gainesville Cohort, 2000

---

## VERSION HISTORY

- v1.0 (2025-10-27): Initial documentation from firsthand account
- Future versions: Awaiting community implementation and feedback

---

## LICENSE

This specification is released into the public domain. The knowledge gained through struggle and innovation belongs to everyone.

Use it. Adapt it. Evolve it. Teach with it.

The game continues.
