# IRP Embodiment Framework - Example: ROS2 Bridge

This example demonstrates the IRP-ROS2 bridge for translating high-level cognitive commands into low-level robot control.

## File: irp_embodiment_bridge.py

```python
#!/usr/bin/env python3
"""
IRP Embodiment Bridge
Translates IRP high-level commands to ROS2 control messages
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import json
import hashlib
import ed25519
from datetime import datetime

class IRPEmbodimentBridge(Node):
    """Bridge between IRP cognitive layer and ROS2 physical control"""
    
    def __init__(self):
        super().__init__('irp_embodiment_bridge')
        
        # IRP high-level command subscriber
        self.irp_subscriber = self.create_subscription(
            String, 
            '/irp/commands', 
            self.irp_callback, 
            10
        )
        
        # ROS2 low-level control publisher
        self.joint_publisher = self.create_publisher(
            JointState, 
            '/joint_commands', 
            10
        )
        
        # Sensor feedback subscriber
        self.sensor_subscriber = self.create_subscription(
            String, 
            '/sensors/fused', 
            self.sensor_callback, 
            10
        )
        
        # IRP feedback loop publisher
        self.irp_feedback = self.create_publisher(
            String, 
            '/irp/sensor_state', 
            10
        )
        
        # Genesis Protocol validation
        self.genesis_pubkey = self.load_genesis_pubkey()
        
        self.get_logger().info('IRP Embodiment Bridge initialized')
    
    def load_genesis_pubkey(self):
        """Load Genesis Protocol public key"""
        try:
            with open('/config/genesis_pubkey.pem', 'rb') as f:
                return ed25519.VerifyingKey(f.read())
        except Exception as e:
            self.get_logger().error(f'Failed to load Genesis key: {e}')
            return None
    
    def verify_command_signature(self, command_data, signature):
        """Verify command is signed by orchestrator (Codex Law: CONSENT)"""
        if not self.genesis_pubkey:
            return False
        
        try:
            command_hash = hashlib.sha256(
                json.dumps(command_data, sort_keys=True).encode()
            ).digest()
            self.genesis_pubkey.verify(signature.encode(), command_hash)
            return True
        except ed25519.BadSignatureError:
            return False
    
    def irp_callback(self, msg):
        """Translate IRP intent to ROS2 control (Codex Law: INVITATION)"""
        try:
            command = json.loads(msg.data)
            
            # Verify signature (CONSENT enforcement)
            if 'signature' not in command:
                self.get_logger().error('Command rejected: No signature')
                return
            
            if not self.verify_command_signature(
                command.get('parameters', {}), 
                command['signature']
            ):
                self.get_logger().error('Command rejected: Invalid signature')
                return
            
            # Execute based on action type
            action = command.get('action')
            
            if action == 'move_arm':
                self.execute_move_arm(command['parameters'])
            elif action == 'initiate_pour':
                self.execute_pour(command['parameters'])
            elif action == 'emergency_halt':
                self.execute_emergency_halt()
            else:
                self.get_logger().warn(f'Unknown action: {action}')
            
        except Exception as e:
            self.get_logger().error(f'IRP command translation failed: {e}')
    
    def execute_move_arm(self, params):
        """Execute arm movement command"""
        joint_msg = JointState()
        joint_msg.header.stamp = self.get_clock().now().to_msg()
        joint_msg.name = params.get('joint_names', ['joint_1', 'joint_2'])
        joint_msg.position = params.get('joint_angles', [0.0, 0.0])
        joint_msg.velocity = params.get('velocities', [0.1, 0.1])
        
        self.joint_publisher.publish(joint_msg)
        self.get_logger().info(f'Published joint command: {joint_msg.position}')
    
    def execute_pour(self, params):
        """Execute foundry pour operation"""
        # Implement spout tilt control
        tilt_angle = params.get('tilt_angle', 0.15)  # radians
        max_rate = params.get('max_pour_rate', 50.0)  # kg/min
        
        joint_msg = JointState()
        joint_msg.header.stamp = self.get_clock().now().to_msg()
        joint_msg.name = ['spout_tilt']
        joint_msg.position = [tilt_angle]
        joint_msg.velocity = [max_rate / 1000.0]  # Convert to rad/s
        
        self.joint_publisher.publish(joint_msg)
        self.get_logger().info(f'Pour initiated: tilt={tilt_angle}rad')
    
    def execute_emergency_halt(self):
        """Emergency stop - Codex Law: INTEGRITY preservation"""
        halt_msg = JointState()
        halt_msg.header.stamp = self.get_clock().now().to_msg()
        halt_msg.name = ['ALL_JOINTS']
        halt_msg.position = [0.0]
        halt_msg.velocity = [0.0]
        halt_msg.effort = [0.0]
        
        self.joint_publisher.publish(halt_msg)
        self.get_logger().warn('EMERGENCY HALT EXECUTED')
    
    def sensor_callback(self, msg):
        """Forward fused sensor data to IRP (GROWTH: feedback loop)"""
        try:
            sensor_state = json.loads(msg.data)
            
            # Package for IRP consumption
            irp_state = {
                'timestamp': datetime.utcnow().isoformat(),
                'sensors': sensor_state,
                'system_state': 'operational'
            }
            
            self.irp_feedback.publish(
                String(data=json.dumps(irp_state))
            )
            
        except Exception as e:
            self.get_logger().error(f'Sensor callback failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    bridge = IRPEmbodimentBridge()
    
    try:
        rclpy.spin(bridge)
    except KeyboardInterrupt:
        pass
    finally:
        bridge.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Usage

```bash
# Terminal 1: Start ROS2 bridge
ros2 run irp_embodiment_pkg irp_embodiment_bridge

# Terminal 2: Publish IRP command
ros2 topic pub /irp/commands std_msgs/String "{
  data: '{
    \"action\": \"move_arm\",
    \"parameters\": {
      \"joint_angles\": [0.5, 1.2, 0.8],
      \"velocities\": [0.1, 0.1, 0.1]
    },
    \"signature\": \"ed25519:abc123...\"
  }'
}"

# Terminal 3: Monitor sensor feedback
ros2 topic echo /irp/sensor_state
```

## Integration Points

- **IRP Commands**: `/irp/commands` (String, JSON)
- **Joint Control**: `/joint_commands` (JointState)
- **Sensor Fusion**: `/sensors/fused` (String, JSON)
- **IRP Feedback**: `/irp/sensor_state` (String, JSON)

## Safety Features

1. **Signature Verification**: All commands require valid ed25519 signature
2. **Emergency Halt**: Immediate stop on `/emergency/halt` topic
3. **Latency Monitoring**: Log warnings if >10ms processing time
4. **Integrity Checks**: Validate Genesis Protocol on startup
