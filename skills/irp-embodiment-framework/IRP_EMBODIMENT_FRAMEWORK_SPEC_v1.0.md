# IRP Embodiment Framework Specification
**Version:** 1.0.0  
**Date:** 2025-12-07  
**Status:** ACTIVE  
**Document ID:** IRP-EMB-SPEC-001

---

## Executive Summary

This framework extends the Intelligent Response Protocol (IRP) into physical embodiment, bridging high-level cognitive orchestration with real-time sensor fusion and actuator control. It synthesizes specifications from the Embodied AI Genesis Protocol, foundry AR operations requirements, and hardware architecture audits to create a sovereignty-preserving, latency-optimized system for robotics and industrial operations.

**Core Principle:** The mental model (cognition) remains form-factor agnostic while the embodiment layer adapts to physical modalities (humanoid, AR overlay, industrial sensors).

---

## 1. Architecture Overview

### 1.1 Layered Design

```
┌─────────────────────────────────────────────────────┐
│  LAYER 4: Cognitive Orchestration (IRP Swarm)       │
│  - Multi-agent deliberation (Claude, Gemini, etc.)  │
│  - XML/JSON protocol-based communication            │
│  - High-level planning & ethical reasoning          │
└─────────────────────────────────────────────────────┘
                       ↕ (Semantic Bridge)
┌─────────────────────────────────────────────────────┐
│  LAYER 3: Embodiment Translation Layer (NEW)        │
│  - Real-world data ingestion (sensors)              │
│  - Command translation (intent → actions)           │
│  - Temporal sequencing & coordination               │
│  - Safety boundary enforcement                      │
└─────────────────────────────────────────────────────┘
                       ↕ (Control Bridge)
┌─────────────────────────────────────────────────────┐
│  LAYER 2: Real-Time Control Substrate               │
│  - ROS2 middleware on RTOS                          │
│  - Kinematic solvers & PID loops                    │
│  - Hardware abstraction (motors, sensors)           │
│  - <10ms response guarantee                         │
└─────────────────────────────────────────────────────┘
                       ↕ (Hardware I/O)
┌─────────────────────────────────────────────────────┐
│  LAYER 1: Physical Modality                         │
│  - Humanoid actuators OR                            │
│  - AR overlay systems OR                            │
│  - Industrial sensors (acoustic, weight, thermal)   │
└─────────────────────────────────────────────────────┘
```

### 1.2 Critical Constraints (Codex Law Enforcement)

| Principle | Implementation |
|-----------|----------------|
| **CONSENT** | All physical actions require signed orchestrator intent |
| **INVITATION** | System operates only when addressed/triggered |
| **INTEGRITY** | Cryptographic validation chain from ethics core to actuators |
| **GROWTH** | Incremental capability expansion with audit trails |

**Additional Constraints:**
- **Sovereignty:** All processing occurs on local hardware (Mac Studio M1 Max 64GB)
- **Latency:** <10ms for safety-critical reflexes; <50ms for deliberative actions
- **Fail-Safe:** Degradation to non-operational state on integrity/tracking failure

---

## 2. Hardware Specification

### 2.1 Validated Configuration

**PRIMARY NODE (MONOLITHIC ARCHITECTURE):**
```yaml
Platform: Mac Studio M1 Max
RAM: 64GB Unified Memory
Storage: 2TB SSD (NVMe)
Compute: 10-core CPU, 32-core GPU, 16-core Neural Engine
Cost: ~$1,450 (refurbished)

Rationale:
  - Unified memory eliminates PCIe latency for sensor fusion
  - Sufficient VRAM for local LLM inference (Gemma 27B quantized)
  - Neural Engine accelerates CV pipelines (acoustic spectrograms, visual tracking)
  - Single node avoids "split-brain" failure modes in robotics
```

**REJECT CLUSTERING:**  
Daisy-chaining via Thunderbolt introduces 1-5ms+ latency and stuttering—fatal for real-time balance/reflex loops. Second machine only justified after first saturates (OOM).

### 2.2 Peripheral Hardware

**For AR Foundry Operations:**
- Meta Quest 3 (AR overlay, hand tracking)
- TPM 2.0 module (Infineon OPTIGA SLB9670) for Genesis Protocol validation
- Industrial sensors:
  - Acoustic monitoring (Arduino-based, existing system)
  - Weight sensors (Bluetooth-enabled, existing protocol)
  - Thermal cameras (FLIR Lepton for molten metal)

**For Humanoid Embodiment (Future):**
- Unitree G1 EDU ($16K+) or Figure 03 (TBD pricing)
- External compute handled by Mac Studio via ROS2 bridge

---

## 3. Software Stack

### 3.1 Operating System Selection

**RECOMMENDED: Linux with PREEMPT_RT Patch**

```yaml
Base OS: Ubuntu 24.04 ARM64 (via Asahi Linux on M1)
Kernel: 6.x with PREEMPT_RT patch
Latency: ~100μs (soft real-time)
Justification:
  - Full ROS2 Jazzy support
  - Leverage existing CCNA networking expertise
  - Sovereignty via air-gapped configuration
  - Familiar toolchain (Python, C++, Docker)
```

**ALTERNATIVE: Zephyr RTOS** (for bare-metal embedded)
- Use case: Dedicated microcontroller for safety-critical loops
- Bridge to Mac Studio via serial/CAN bus

### 3.2 Middleware & Frameworks

#### 3.2.1 ROS2 (Robot Operating System 2)

```bash
# Installation on Ubuntu ARM64
sudo apt install ros-jazzy-desktop-full
sudo apt install ros-jazzy-ros2-control ros-jazzy-ros2-controllers

# Real-time configuration
sudo usermod -a -G realtime $USER
sudo nano /etc/security/limits.conf
# Add: @realtime soft rtprio 99
# Add: @realtime soft memlock unlimited
```

**Key ROS2 Packages for IRP:**
- `ros2_control`: Hardware abstraction for actuators
- `moveit2`: Motion planning for humanoids
- `nav2`: Autonomous navigation
- `sensor_msgs`: Standardized sensor data types
- `tf2`: Coordinate frame transformations

#### 3.2.2 IRP-ROS2 Bridge Architecture

```python
# Conceptual bridge: irp_swarm → ROS2
# File: irp_embodiment_bridge.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import json

class IRPEmbodimentBridge(Node):
    def __init__(self):
        super().__init__('irp_embodiment_bridge')
        
        # Subscribe to IRP high-level commands (from swarm)
        self.irp_subscriber = self.create_subscription(
            String, '/irp/commands', self.irp_callback, 10)
        
        # Publish to ROS2 control (low-level)
        self.joint_publisher = self.create_publisher(
            JointState, '/joint_commands', 10)
        
        # Subscribe to sensor feedback
        self.sensor_subscriber = self.create_subscription(
            String, '/sensors/fused', self.sensor_callback, 10)
        
        # Publish to IRP (feedback loop)
        self.irp_feedback = self.create_publisher(
            String, '/irp/sensor_state', 10)
    
    def irp_callback(self, msg):
        """Translate IRP JSON/XML to ROS2 control commands"""
        try:
            command = json.loads(msg.data)
            # Example: {"action": "move_arm", "joint_angles": [0.5, 1.2, ...]}
            
            if command['action'] == 'move_arm':
                joint_msg = JointState()
                joint_msg.position = command['joint_angles']
                self.joint_publisher.publish(joint_msg)
                
        except Exception as e:
            self.get_logger().error(f'IRP command translation failed: {e}')
    
    def sensor_callback(self, msg):
        """Forward fused sensor data to IRP swarm"""
        sensor_state = json.loads(msg.data)
        # Repackage for IRP XML schema
        self.irp_feedback.publish(String(data=json.dumps(sensor_state)))
```

**Data Flow:**
1. IRP Swarm outputs intent (XML/JSON) → `/irp/commands`
2. Bridge translates to ROS2 messages → `/joint_commands`
3. `ros2_control` executes on hardware
4. Sensors publish to `/sensors/fused`
5. Bridge forwards to `/irp/sensor_state` → Swarm updates mental model

---

## 4. Real-World Data Translation

### 4.1 Sensor Integration Points

```python
# Sensor Fusion Node (ROS2)
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature
from std_msgs.msg import Float64, String
import json
from datetime import datetime

class SensorFusionNode(Node):
    def __init__(self):
        super().__init__('sensor_fusion_node')
        
        # Acoustic (Arduino via serial)
        self.create_subscription(Float64, '/acoustic/anomaly', self.acoustic_cb, 10)
        
        # Weight (Bluetooth loadcells)
        self.create_subscription(Float64, '/weight/current', self.weight_cb, 10)
        
        # Thermal (FLIR camera)
        self.create_subscription(Temperature, '/thermal/max', self.thermal_cb, 10)
        
        # Fused output to IRP
        self.fused_pub = self.create_publisher(String, '/sensors/fused', 10)
        
        self.state = {'acoustic': None, 'weight': None, 'thermal': None}
    
    def acoustic_cb(self, msg):
        self.state['acoustic'] = msg.data
        self.fuse_and_publish()
    
    def weight_cb(self, msg):
        self.state['weight'] = msg.data
        self.fuse_and_publish()
    
    def thermal_cb(self, msg):
        self.state['thermal'] = msg.temperature
        self.fuse_and_publish()
    
    def fuse_and_publish(self):
        if all(v is not None for v in self.state.values()):
            fused_risk = self.calculate_risk_score(self.state)
            
            output = {
                'timestamp': datetime.utcnow().isoformat(),
                'fused_risk': fused_risk,
                'raw_sensors': self.state
            }
            
            self.fused_pub.publish(String(data=json.dumps(output)))
    
    def calculate_risk_score(self, sensors):
        # Weighted combination (tune from training data)
        risk = (
            0.4 * sensors['acoustic'] +
            0.3 * min(sensors['thermal'] / 1400.0, 1.0) +
            0.3 * (abs(sensors['weight'] - 1452.0) / 1452.0)
        )
        return min(risk, 1.0)
```

---

## 5. Safety-Critical Protocols

### 5.1 Genesis Protocol Integration

```python
import hashlib
import ed25519
from datetime import datetime

def validate_embodiment_integrity(ethical_core_path, genesis_pubkey, signature):
    """
    Validates embodiment subsystem against Genesis Protocol
    HALT system if validation fails
    """
    # 1. Hash ethical core
    with open(ethical_core_path, 'rb') as f:
        core_hash = hashlib.sha256(f.read()).hexdigest()
    
    # 2. Verify signature
    try:
        verifying_key = ed25519.VerifyingKey(genesis_pubkey)
        verifying_key.verify(signature, core_hash.encode())
    except ed25519.BadSignatureError:
        print("HALT: Genesis signature validation failed")
        trigger_system_halt()
        return False
    
    # 3. Check monotonic time (prevent rollback attacks)
    genesis_timestamp = get_genesis_timestamp()
    if datetime.utcnow() < genesis_timestamp:
        print("HALT: Time rollback detected")
        trigger_system_halt()
        return False
    
    print("Embodiment validation: PASS")
    return True

def trigger_system_halt():
    """Emergency halt for integrity failures"""
    # ROS2: Publish emergency stop
    # Hardware: Engage brakes/cut power via watchdog
    # AR: Display critical warning overlay
    pass
```

### 5.2 Fail-Safe Degradation

| Failure Mode | Detection | Response | Recovery |
|--------------|-----------|----------|----------|
| AR Tracking Loss | Confidence < 0.8 | Freeze overlays, haptic alert | Require recalibration |
| Sensor Fusion Discrepancy | Weight vs Visual > 5% | Flag anomaly, request human verification | Log for training |
| Actuator Timeout | Command ACK > 50ms | Emergency stop, revert to safe pose | Diagnostic mode |
| Thermal Threshold | Temp > 1400°C | Audible alarm, prevent approach | Cooldown period |
| Integrity Hash Mismatch | Boot validation fail | System halt | Reflash firmware |

### 5.3 Foundry-Specific Safety (3200lb Molten Metal)

**PRE-OPERATION CHECKLIST:**
```yaml
- [ ] Coordinate calibration verified (4 fixed points)
- [ ] Splash zone boundaries defined in 3D
- [ ] Acoustic baseline captured (ambient)
- [ ] Weight sensor zeroed
- [ ] Thermal camera functional test
- [ ] AR tracking confidence > 0.95
- [ ] Emergency stop accessible within 2 seconds
- [ ] Operator wearing protective gear (thermal + AR headset)
- [ ] Backup observer present (two-person rule)
```

**REAL-TIME MONITORING:**
```python
def foundry_safety_loop():
    """1Hz safety check during pour operations"""
    while operation_active:
        state = get_embodiment_state()
        
        # Check thermal boundaries
        if state['thermal_max'] > 1400:
            trigger_alarm("Thermal threshold exceeded")
        
        # Verify AR tracking
        if state['ar_tracking_confidence'] < 0.8:
            freeze_overlays()
            alert_operator("Tracking degraded - rely on visual")
        
        # Weight-visual correlation
        weight_discrepancy = abs(
            state['weight_current'] - state['visual_estimate']
        ) / state['weight_current']
        if weight_discrepancy > 0.05:
            log_anomaly("Weight-visual mismatch", state)
        
        time.sleep(1.0)
```

---

## 6. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)

**Objectives:**
- Set up Mac Studio with Ubuntu + PREEMPT_RT
- Install ROS2 Jazzy with ros2_control
- Validate hardware (TPM, sensors)
- Implement basic IRP-ROS2 bridge

**Deliverables:**
```
✓ Bootable Ubuntu ARM64 with <100μs latency
✓ ROS2 workspace with custom packages
✓ Python bridge publishing to /irp/commands
✓ Sensor data flowing to /sensors/fused
✓ Genesis Protocol boot validation
```

### Phase 2: Sensor Fusion (Weeks 5-8)

**Objectives:**
- Integrate existing acoustic monitoring (Arduino)
- Deploy weight sensor Bluetooth protocol
- Add thermal camera (FLIR Lepton)
- Implement Bayesian fusion algorithm
- Capture 50 foundry sequences

### Phase 3: AR Integration (Weeks 9-12)

**Objectives:**
- Deploy Unity AR container on Meta Quest 3
- Implement coordinate frame calibration
- Overlay safety boundaries in real-time
- Test in controlled foundry simulation

### Phase 4: Humanoid Preparation (Weeks 13-16)

**Objectives:**
- Acquire Unitree G1 (or equivalent)
- Port IRP bridge to humanoid control
- Implement balance/reflex loops (<10ms)
- Safety validation in isolated environment

### Phase 5: Production Deployment (Weeks 17+)

**Objectives:**
- Deploy AR system in live foundry operations
- Continuous data collection for model refinement
- Incremental humanoid capability expansion
- Fleet management for multiple embodiments

---

## 7. Dataset Requirements

### 7.1 Foundry Operations Dataset

**Minimum Viable Dataset:**
```yaml
Normal Operations: 20 sequences
  - Full pour cycle (spout placement → pour → retraction)
  - Synchronized: Acoustic + Weight + Thermal + AR tracking
  - Duration: ~2-5 minutes each

Near-Miss Incidents: 10 sequences
  - Splash events (no injury)
  - Equipment anomalies
  - Weight discrepancies

Critical Anomalies: 5 sequences
  - Equipment failures
  - Thermal excursions
  - Tracking loss during critical phase
```

---

## 8. Governance & Audit

### 8.1 Codex Law Enforcement Mechanisms

```python
from enum import Enum
from datetime import datetime

class CodexPrinciple(Enum):
    CONSENT = "All actions require explicit orchestrator authorization"
    INVITATION = "System operates only when addressed"
    INTEGRITY = "Cryptographic validation chain preserved"
    GROWTH = "Incremental changes with full audit trail"

class CodexViolation(Exception):
    pass

def enforce_consent(action_intent, orchestrator_signature):
    """Verify cryptographic signature on action intent"""
    if not verify_ed25519_signature(action_intent, orchestrator_signature):
        raise CodexViolation("CONSENT violated: Invalid signature")
    
    log_audit_event({
        'principle': CodexPrinciple.CONSENT,
        'action': action_intent,
        'timestamp': datetime.utcnow(),
        'status': 'approved'
    })
```

### 8.2 Audit Logging

```json
{
  "audit_log_entry": {
    "id": "AL-20251207-170000-001",
    "timestamp": "2025-12-07T17:00:00Z",
    "event_type": "actuator_command",
    "orchestrator": "Joseph",
    "signature": "ed25519:abc123...",
    "action": {
      "type": "move_spout",
      "parameters": {"x": 2.1, "y": 0.8, "z": 1.2}
    },
    "sensor_state_snapshot": {
      "acoustic_anomaly": 0.12,
      "weight": 0.0,
      "thermal_max": 1350.0
    },
    "outcome": "success",
    "latency_ms": 8.3
  }
}
```

---

## 9. Success Criteria

### 9.1 Technical Metrics
- [ ] Latency: 95th percentile < 10ms for reflex actions
- [ ] AR tracking: >0.95 confidence for 10-minute sessions
- [ ] Sensor fusion: Weight-visual correlation within 3% RMS
- [ ] Safety: Zero boundary violations in 100 test runs

### 9.2 Operational Metrics
- [ ] 30 days continuous operation without integrity failures
- [ ] Zero molten metal incidents with AR system active
- [ ] Model retraining improves performance by >5% per cycle

---

## Appendix: File Structure

```
irp_embodiment/
├── README.md
├── LICENSE
├── .gitignore
│
├── schemas/
│   ├── embodiment_state.xsd
│   └── embodiment_state.schema.json
│
├── src/
│   ├── ros2_packages/
│   │   ├── irp_embodiment_pkg/
│   │   │   ├── irp_embodiment_bridge.py
│   │   │   ├── sensor_fusion_node.py
│   │   │   ├── safety_monitor_node.py
│   │   │   └── genesis_validator.py
│   │   └── ...
│   │
│   ├── unity/
│   │   └── IRPAROverlay/
│   │
│   └── training/
│       ├── gemma_foundry_finetune.py
│       └── dataset_processor.py
│
├── config/
│   ├── genesis_core.xml
│   ├── genesis_pubkey.pem
│   └── safety_parameters.yaml
│
├── data/
│   ├── foundry_sequences/
│   ├── calibration/
│   └── audit_logs/
│
└── docs/
    ├── SAFETY_PROTOCOLS.md
    ├── API_REFERENCE.md
    └── TROUBLESHOOTING.md
```

---

**Document Status:** ACTIVE  
**Next Action:** Implementation Phase 1  
**Transmission Packet Compatible:** Yes

---

END OF SPECIFICATION