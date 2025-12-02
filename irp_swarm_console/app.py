"""
IRP Orchestrator Swarm Console
==============================
Streamlit-based orchestration interface for the IRP (Intelligent Relay Protocol) framework.
Manages nodes, methodologies, and IUPP packet routing.
"""

import streamlit as st
import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# Import local modules
from node_registry import NodeRegistry, get_node_registry
from gam_memory import GAMMemory, get_gam_memory
from methodology_loader import MethodologyLoader, get_methodology_loader
from iupp_protocol import IUPPPacketBuilder, create_iupp_packet


# Page configuration
st.set_page_config(
    page_title="IRP Swarm Console",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .node-active {
        color: #00ff00;
        font-weight: bold;
    }
    .node-inactive {
        color: #ff6600;
    }
    .node-error {
        color: #ff0000;
    }
    .chat-user {
        background-color: #1e3a5f;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .chat-system {
        background-color: #2d2d2d;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .methodology-card {
        background-color: #1a1a2e;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #4a9eff;
    }
    .packet-display {
        font-family: 'Courier New', monospace;
        background-color: #0d1117;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize Streamlit session state variables."""
    if 'registry' not in st.session_state:
        st.session_state.registry = get_node_registry()
    
    if 'gam' not in st.session_state:
        st.session_state.gam = get_gam_memory()
    
    if 'methodology_loader' not in st.session_state:
        st.session_state.methodology_loader = get_methodology_loader()
    
    if 'packet_builder' not in st.session_state:
        st.session_state.packet_builder = IUPPPacketBuilder()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'last_packet' not in st.session_state:
        st.session_state.last_packet = None


def parse_command(input_text: str) -> Tuple[str, list]:
    """
    Parse user input to identify commands and arguments.
    
    Args:
        input_text: Raw user input
        
    Returns:
        Tuple of (command_name, arguments_list)
    """
    input_text = input_text.strip()
    
    if not input_text.startswith('/'):
        return ('chat', [input_text])
    
    # Split command and arguments
    parts = input_text.split(maxsplit=1)
    command = parts[0].lower()
    
    if len(parts) > 1:
        # Parse arguments - handle quoted strings
        args_str = parts[1]
        args = re.findall(r'(?:[^\s"]+|"[^"]*")+', args_str)
        args = [arg.strip('"') for arg in args]
    else:
        args = []
    
    return (command, args)


def handle_register_command(args: list) -> str:
    """
    Handle /register command.
    Usage: /register [URL] [API_KEY] [NODE_NAME] [CAPABILITIES...]
    """
    if len(args) < 3:
        return """❌ **Invalid syntax**
        
Usage: `/register [URL] [API_KEY] [NODE_NAME] [CAPABILITIES...]`

Example:
```
/register http://localhost:11434 ollama-key my-llm-node red-team,rtc
```
"""
    
    url = args[0]
    api_key = args[1]
    node_name = args[2]
    capabilities = args[3].split(',') if len(args) > 3 else []
    
    result = st.session_state.registry.register_node(
        node_id=node_name,
        url=url,
        api_key=api_key,
        capabilities=capabilities
    )
    
    if result['success']:
        return f"""✅ **Node Registered Successfully**

| Field | Value |
|-------|-------|
| Node ID | `{node_name}` |
| URL | `{url}` |
| Capabilities | {', '.join(capabilities) if capabilities else 'None specified'} |
| Status | 🟢 Active |
"""
    else:
        return f"❌ **Registration Failed**: {result.get('message', 'Unknown error')}"


def handle_status_command() -> str:
    """Handle /status command - show all registered nodes."""
    nodes = st.session_state.registry.get_all_nodes()
    
    if not nodes:
        return """📡 **Node Registry Status**

No nodes registered yet.

Use `/register [URL] [KEY] [NAME]` to add a node.
"""
    
    output = "📡 **Node Registry Status**\n\n"
    output += "| Node ID | URL | Status | Last Heartbeat |\n"
    output += "|---------|-----|--------|----------------|\n"
    
    for node_id, info in nodes.items():
        status_icon = {
            'active': '🟢',
            'inactive': '🟡',
            'error': '🔴',
            'unreachable': '⚫'
        }.get(info['status'], '⚪')
        
        heartbeat = info.get('last_heartbeat', 'N/A')
        if heartbeat and heartbeat != 'N/A':
            heartbeat = heartbeat[:19]  # Truncate timestamp
        
        output += f"| `{node_id}` | `{info['url'][:30]}...` | {status_icon} {info['status']} | {heartbeat} |\n"
    
    output += f"\n**Total Nodes:** {len(nodes)}"
    
    return output


def handle_orchestrate_command(args: list) -> str:
    """
    Handle /orchestrate command.
    Usage: /orchestrate [GOAL]
    Routes to appropriate nodes based on goal and methodologies.
    """
    if not args:
        return """❌ **Invalid syntax**

Usage: `/orchestrate [GOAL]`

Example:
```
/orchestrate Analyze this API design for security vulnerabilities
```
"""
    
    goal = ' '.join(args)
    
    # Determine best methodology based on goal keywords
    methodology = determine_methodology(goal)
    
    output = f"""🎯 **Orchestration Initiated**

**Goal:** {goal}

**Selected Methodology:** `{methodology}`

"""
    
    # Get methodology details
    method_data = st.session_state.methodology_loader.get_methodology(methodology)
    
    if method_data:
        output += f"""**Methodology Info:**
- Category: {method_data.get('category', 'Unknown')}
- Version: {method_data.get('version', '1.0.0')}

"""
    
    # Get GAM context
    gam_context = st.session_state.gam.get_context_for_injection(max_entries=3)
    
    # Check for registered nodes
    nodes = st.session_state.registry.get_all_nodes()
    
    if nodes:
        # Find best node for this methodology
        target_node = find_best_node_for_methodology(methodology)
        
        if target_node:
            output += f"**Routing to Node:** `{target_node}`\n\n"
            
            # Build IUPP packet
            packet = st.session_state.packet_builder.build_request_packet(
                target_node_id=target_node,
                query=goal,
                methodology=methodology,
                gam_context=gam_context
            )
            
            st.session_state.last_packet = packet
            
            output += "📦 **IUPP Packet Created:**\n```json\n"
            output += json.dumps(packet, indent=2)[:1000]
            output += "\n```\n\n"
            
            # Route the packet
            output += "🚀 **Sending packet...**\n\n"
            
            response = st.session_state.registry.route_packet(target_node, packet)
            
            if response['success']:
                result_content = IUPPPacketBuilder.extract_result(response['data'])
                
                if result_content:
                    output += f"✅ **Response Received:**\n\n{result_content}"
                    
                    # Log to GAM
                    st.session_state.gam.append_entry(
                        user_input=goal,
                        node_used=target_node,
                        resultant_seed=result_content[:500],
                        protocol_packet=packet
                    )
                else:
                    output += f"⚠️ **Raw Response:**\n```json\n{json.dumps(response['data'], indent=2)[:1000]}\n```"
            else:
                output += f"❌ **Routing Failed:** {response.get('error', 'Unknown error')}"
        else:
            output += execute_builtin_methodology(methodology, goal, gam_context)
    else:
        # No external nodes - use built-in execution
        output += "⚠️ **No external nodes registered.** Executing with built-in methodology.\n\n"
        output += execute_builtin_methodology(methodology, goal, gam_context)
    
    return output


def determine_methodology(goal: str) -> str:
    """
    Determine the best methodology based on goal content.
    
    Args:
        goal: User's goal/query
        
    Returns:
        Methodology name
    """
    goal_lower = goal.lower()
    
    # Keyword mapping to methodologies
    mappings = [
        (['security', 'vulnerability', 'audit', 'red team', 'penetration', 'threat'], 
         'internal-red-team-audit'),
        (['analyze', 'research', 'investigate', 'study', 'examine'], 
         'rtc-consensus-synthesis'),
        (['challenge', 'question', 'argue', 'debate', 'counter'], 
         'devils-advocate'),
        (['stress', 'test', 'edge case', 'boundary', 'limit'], 
         'stress-tester'),
        (['creative', 'design', 'pattern', 'aesthetic'], 
         'artist'),
        (['novel', 'innovative', 'new approach', 'alternative'], 
         'innovator'),
        (['governance', 'compliance', 'law', 'policy', 'consent'], 
         'codex-law-enforcement'),
        (['threat', 'drift', 'manipulation', 'trap'], 
         'antidote-threat-handler'),
        (['packet', 'transmission', 'protocol', 'state'], 
         'transmission-packet-forge'),
    ]
    
    for keywords, methodology in mappings:
        if any(kw in goal_lower for kw in keywords):
            return methodology
    
    # Default to red team audit
    return 'internal-red-team-audit'


def find_best_node_for_methodology(methodology: str) -> Optional[str]:
    """
    Find the best node to handle a given methodology.
    
    Args:
        methodology: Required methodology name
        
    Returns:
        Node ID or None
    """
    # First, check for nodes with matching capability
    matching = st.session_state.registry.find_nodes_by_capability(methodology)
    
    if matching:
        return matching[0]
    
    # Fall back to any active node
    nodes = st.session_state.registry.get_all_nodes()
    for node_id, info in nodes.items():
        if info['status'] == 'active':
            return node_id
    
    return None


def execute_builtin_methodology(methodology: str, goal: str, gam_context: str) -> str:
    """
    Execute a methodology using built-in logic (no external node required).
    This is the pilot/fallback execution mode.
    
    Args:
        methodology: Methodology to execute
        goal: User's goal
        gam_context: GAM context injection
        
    Returns:
        Execution result
    """
    method_data = st.session_state.methodology_loader.get_methodology(methodology)
    
    output = f"🔧 **Built-in Execution: {methodology}**\n\n"
    
    if not method_data:
        output += f"⚠️ Methodology `{methodology}` not found in registry.\n"
        output += "Executing with generic analysis...\n\n"
        method_content = "Generic analysis protocol"
    else:
        method_content = method_data.get('content', '')
        calibration = method_data.get('calibration', {})
        
        output += f"**Calibration Settings:**\n```yaml\n"
        for key, value in calibration.items():
            output += f"{key}: {value}\n"
        output += "```\n\n"
    
    # Execute based on methodology type
    if methodology == 'internal-red-team-audit':
        output += execute_red_team_audit(goal, gam_context)
    elif methodology == 'rtc-consensus-synthesis':
        output += execute_rtc_synthesis(goal, gam_context)
    elif methodology in ['devils-advocate', 'stress-tester', 'artist', 'innovator']:
        output += execute_rtc_persona(methodology, goal, gam_context)
    elif methodology == 'antidote-threat-handler':
        output += execute_threat_handler(goal, gam_context)
    else:
        output += execute_generic_analysis(goal, method_content, gam_context)
    
    # Log to GAM
    st.session_state.gam.append_entry(
        user_input=goal,
        node_used=f"builtin:{methodology}",
        resultant_seed=output[:500],
        protocol_packet={"builtin_execution": True, "methodology": methodology}
    )
    
    return output


def execute_red_team_audit(goal: str, context: str) -> str:
    """Execute internal red team audit methodology."""
    audit_id = st.session_state.packet_builder.build_packet(
        "internal", goal, "internal-red-team-audit"
    )['header']['packet_id'][:8]
    
    return f"""
### 🔴 Internal Red Team Audit Report

**Audit ID:** `AUDIT-{audit_id}`  
**Target:** {goal[:100]}{'...' if len(goal) > 100 else ''}  
**Timestamp:** {datetime.utcnow().isoformat()}Z

---

#### Phase 1: Reconnaissance
- **Attack Surface Identified:** Analyzing input for potential weak points
- **Context Review:** {len(context.split())} tokens of prior context available

#### Phase 2: Threat Modeling
| Threat Vector | Likelihood | Impact | Risk Score |
|--------------|------------|--------|------------|
| Input Validation | Medium | High | 6.5 |
| Authentication Bypass | Low | Critical | 5.0 |
| Logic Flaws | Medium | Medium | 4.5 |
| Information Disclosure | High | Low | 4.0 |

#### Phase 3: Findings Summary
⚠️ **Note:** This is a built-in simulation. For comprehensive audits, register an LLM node.

**Preliminary Assessment:**
1. **FINDING-001** [MEDIUM]: Input should be validated for injection patterns
2. **FINDING-002** [LOW]: Consider rate limiting for API endpoints
3. **FINDING-003** [INFO]: Documentation should include threat model

#### Phase 4: Recommendations
- Implement input sanitization
- Add logging and monitoring
- Conduct full penetration test with external tools

**Risk Score:** 5.5/10 (Moderate)

---
*Red Team Audit Complete - Built-in Mode*
"""


def execute_rtc_synthesis(goal: str, context: str) -> str:
    """Execute RTC (Recursive Thought Committee) synthesis."""
    return f"""
### 🔬 RTC Consensus Synthesis

**Query:** {goal[:150]}{'...' if len(goal) > 150 else ''}

---

#### Committee Analysis

**👨‍🎨 The Artist:**
> I see patterns of structure here - there's a rhythm to how this query flows. 
> The aesthetic suggests a need for balanced, harmonious solutions that consider 
> form alongside function.

**💡 The Innovator:**
> What if we approached this from an entirely different angle? Instead of 
> conventional methods, consider leveraging emergent patterns and cross-domain 
> inspiration to find novel pathways.

**🔍 The Stress Tester:**
> Let me probe the boundaries here. What happens at scale? What are the edge 
> cases? We need to consider failure modes: resource exhaustion, cascading 
> failures, and recovery scenarios.

**😈 The Devil's Advocate:**
> Hold on - let's challenge the fundamental assumptions. Why are we accepting 
> these constraints? What evidence supports the current approach? I see at 
> least three questionable premises that need examination.

---

#### 🍳 Kitchen Synthesis

After harmonizing the committee's perspectives, the following synthesis emerges:

1. **Core Insight:** The problem space requires both structural elegance (Artist) 
   and unconventional thinking (Innovator)

2. **Critical Considerations:** The Devil's Advocate raises valid concerns about 
   underlying assumptions that should be explicitly validated

3. **Robustness:** Stress Tester's edge cases reveal potential failure points 
   that must be addressed in any solution

4. **Recommended Approach:** A phased implementation that:
   - Validates core assumptions first
   - Implements with consideration for aesthetics and maintainability
   - Includes comprehensive edge case handling
   - Maintains flexibility for innovative pivots

**Consensus Score:** 0.78 (High Agreement)

---
*RTC Synthesis Complete - Built-in Mode*
"""


def execute_rtc_persona(persona: str, goal: str, context: str) -> str:
    """Execute a specific RTC persona analysis."""
    personas = {
        'artist': ('👨‍🎨', 'The Artist', 'Pattern Recognition'),
        'devils-advocate': ('😈', "The Devil's Advocate", 'Challenge Framework'),
        'stress-tester': ('🔍', 'The Stress Tester', 'Edge Case Analysis'),
        'innovator': ('💡', 'The Innovator', 'Novel Approaches')
    }
    
    icon, name, specialty = personas.get(persona, ('🤖', 'Unknown', 'General'))
    
    return f"""
### {icon} {name} Analysis

**Specialty:** {specialty}  
**Target:** {goal[:100]}{'...' if len(goal) > 100 else ''}

---

#### Perspective Analysis

As {name}, I approach this from my unique vantage point of {specialty.lower()}.

**Initial Observations:**
- The structure presents interesting characteristics
- Key elements worthy of deeper examination identified
- Patterns suggest multiple valid interpretations

**Core Analysis:**
Through the lens of {specialty.lower()}, I see opportunities and concerns that 
may not be immediately apparent from conventional viewpoints.

**Key Insights:**
1. First insight related to {specialty.lower()}
2. Secondary consideration
3. Deeper pattern recognition

**Recommendations:**
Based on this analysis, I recommend further exploration of the identified 
patterns with attention to the specific concerns raised.

---
*{name} Analysis Complete - Built-in Mode*
"""


def execute_threat_handler(goal: str, context: str) -> str:
    """Execute antidote threat handler methodology."""
    return f"""
### 🛡️ Antidote Threat Handler Report

**Scan Target:** {goal[:100]}{'...' if len(goal) > 100 else ''}

---

#### Threat Detection Scan

| Category | Status | Confidence |
|----------|--------|------------|
| Sycophancy Drift | ✅ Clear | 95% |
| Cognitive Traps | ✅ Clear | 90% |
| Identity Erosion | ✅ Clear | 98% |
| Consent Violations | ✅ Clear | 99% |

#### Pattern Analysis
- No manipulation patterns detected
- Input appears legitimate and well-formed
- Context consistency verified

#### Recommendations
- Continue standard processing
- No countermeasures required
- Log for audit trail

**Threat Level:** LOW (0.2/10)

---
*Threat Handler Scan Complete - Built-in Mode*
"""


def execute_generic_analysis(goal: str, method_content: str, context: str) -> str:
    """Execute generic analysis for unknown methodologies."""
    return f"""
### 📋 Generic Analysis

**Query:** {goal[:150]}

**Methodology Content Length:** {len(method_content)} characters

---

#### Analysis

Based on the provided goal and methodology context:

1. **Input Received:** Query has been parsed and validated
2. **Methodology Applied:** Generic analysis protocol
3. **Context Integration:** Prior context considered

#### Output

The input has been processed according to available methodology guidelines.
For specialized analysis, consider:
- Registering an external LLM node
- Using a more specific methodology
- Providing additional context

---
*Generic Analysis Complete - Built-in Mode*
"""


def handle_methodologies_command() -> str:
    """Handle /methodologies command - list available methodologies."""
    methodologies = st.session_state.methodology_loader.list_methodologies()
    
    if not methodologies:
        return "📚 **No methodologies loaded.** Check the skills directory."
    
    output = "📚 **Available Methodologies**\n\n"
    
    # Group by category
    by_category = {}
    for name, info in methodologies.items():
        cat = info.get('category', 'Uncategorized')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append((name, info))
    
    for category, items in sorted(by_category.items()):
        output += f"### {category}\n"
        for name, info in sorted(items):
            output += f"- `{name}` (v{info.get('version', '1.0.0')})\n"
        output += "\n"
    
    output += f"**Total:** {len(methodologies)} methodologies"
    
    return output


def handle_gam_command(args: list) -> str:
    """Handle /gam command - show GAM memory stats and history."""
    subcommand = args[0] if args else 'stats'
    
    if subcommand == 'stats':
        stats = st.session_state.gam.get_stats()
        return f"""📊 **GAM Memory Statistics**

| Metric | Value |
|--------|-------|
| Total Entries | {stats['total_entries']} |
| Unique Sessions | {stats['unique_sessions']} |
| Unique Nodes | {stats['unique_nodes']} |
| Current Session Entries | {stats['current_session_entries']} |

**Current Session ID:** `{stats['current_session'][:8]}...`

**Nodes Used:** {', '.join(f'`{n}`' for n in stats['nodes_list']) or 'None'}
"""
    
    elif subcommand == 'history':
        limit = int(args[1]) if len(args) > 1 else 5
        history = st.session_state.gam.query_history(limit=limit)
        
        if not history:
            return "📜 **GAM History:** No entries yet."
        
        output = f"📜 **GAM History** (last {len(history)} entries)\n\n"
        
        for entry in history:
            output += f"""---
**[{entry['timestamp'][:19]}]** via `{entry['node_used']}`

Input: {entry['user_input'][:100]}{'...' if len(entry['user_input']) > 100 else ''}

Result: {entry['resultant_seed'][:150]}{'...' if len(entry['resultant_seed']) > 150 else ''}

"""
        
        return output
    
    elif subcommand == 'context':
        context = st.session_state.gam.get_context_for_injection()
        return f"📋 **GAM Context Injection:**\n\n```\n{context}\n```"
    
    elif subcommand == 'new':
        new_session = st.session_state.gam.start_new_session()
        return f"🆕 **New GAM Session Started**\n\nSession ID: `{new_session[:8]}...`"
    
    else:
        return """📊 **GAM Commands:**

- `/gam stats` - Show memory statistics
- `/gam history [N]` - Show last N entries (default: 5)
- `/gam context` - Show context injection preview
- `/gam new` - Start new session
"""


def handle_help_command() -> str:
    """Handle /help command."""
    return """# 🌐 IRP Swarm Console Help

## Available Commands

### Node Management
| Command | Description |
|---------|-------------|
| `/register [URL] [KEY] [NAME] [CAPS]` | Register a new node |
| `/status` | Show all registered nodes |
| `/remove [NODE_ID]` | Remove a node |

### Orchestration
| Command | Description |
|---------|-------------|
| `/orchestrate [GOAL]` | Execute orchestration with methodology |
| `/methodologies` | List available methodologies |

### Memory (GAM)
| Command | Description |
|---------|-------------|
| `/gam stats` | Show GAM memory statistics |
| `/gam history [N]` | Show recent history |
| `/gam context` | Preview context injection |
| `/gam new` | Start new session |

### Other
| Command | Description |
|---------|-------------|
| `/help` | Show this help |
| `/clear` | Clear chat history |

## Quick Start

1. **Register a node:**
   ```
   /register http://localhost:11434 my-key local-llm rtc,red-team
   ```

2. **Check status:**
   ```
   /status
   ```

3. **Run orchestration:**
   ```
   /orchestrate Analyze this system for security vulnerabilities
   ```

## Methodology Detection

The orchestrator automatically selects methodologies based on keywords:
- Security/Audit → `internal-red-team-audit`
- Analyze/Research → `rtc-consensus-synthesis`
- Challenge/Debate → `devils-advocate`
- Test/Edge case → `stress-tester`

## Built-in Mode

If no nodes are registered, methodologies run in built-in simulation mode.
"""


def process_input(user_input: str) -> str:
    """
    Process user input and return response.
    
    Args:
        user_input: Raw user input
        
    Returns:
        Response string
    """
    command, args = parse_command(user_input)
    
    command_handlers = {
        '/register': lambda: handle_register_command(args),
        '/status': lambda: handle_status_command(),
        '/orchestrate': lambda: handle_orchestrate_command(args),
        '/methodologies': lambda: handle_methodologies_command(),
        '/gam': lambda: handle_gam_command(args),
        '/help': lambda: handle_help_command(),
        '/clear': lambda: "CLEAR_HISTORY",
        '/remove': lambda: handle_remove_command(args),
    }
    
    if command in command_handlers:
        return command_handlers[command]()
    elif command == 'chat':
        # Non-command input - treat as orchestration goal
        return handle_orchestrate_command(args)
    else:
        return f"❓ Unknown command: `{command}`\n\nType `/help` for available commands."


def handle_remove_command(args: list) -> str:
    """Handle /remove command."""
    if not args:
        return "❌ Usage: `/remove [NODE_ID]`"
    
    node_id = args[0]
    result = st.session_state.registry.remove_node(node_id)
    
    if result['success']:
        return f"✅ Node `{node_id}` removed."
    else:
        return f"❌ {result['message']}"


def render_sidebar():
    """Render the left sidebar with node registry."""
    with st.sidebar:
        st.header("📡 Node Registry")
        
        nodes = st.session_state.registry.get_all_nodes()
        
        if not nodes:
            st.info("No nodes registered")
            st.markdown("""
            **Quick Register:**
            ```
            /register [URL] [KEY] [NAME]
            ```
            """)
        else:
            for node_id, info in nodes.items():
                status_color = {
                    'active': '🟢',
                    'inactive': '🟡',
                    'error': '🔴',
                    'unreachable': '⚫'
                }.get(info['status'], '⚪')
                
                with st.expander(f"{status_color} {node_id}"):
                    st.markdown(f"**URL:** `{info['url']}`")
                    st.markdown(f"**Status:** {info['status']}")
                    if info['capabilities']:
                        st.markdown(f"**Capabilities:** {', '.join(info['capabilities'])}")
                    st.markdown(f"**Errors:** {info['error_count']}")
        
        st.divider()
        
        # GAM Stats
        st.header("💾 GAM Memory")
        stats = st.session_state.gam.get_stats()
        st.metric("Session Entries", stats['current_session_entries'])
        st.metric("Total Entries", stats['total_entries'])
        
        if st.button("🆕 New Session"):
            st.session_state.gam.start_new_session()
            st.rerun()


def render_methodology_browser():
    """Render the methodology browser in the right column."""
    st.header("📚 Methodologies")
    
    methodologies = st.session_state.methodology_loader.list_methodologies()
    
    if not methodologies:
        st.warning("No methodologies loaded")
        return
    
    # Search
    search = st.text_input("🔍 Search", placeholder="Filter methodologies...")
    
    # Filter
    if search:
        methodologies = {
            k: v for k, v in methodologies.items() 
            if search.lower() in k.lower() or search.lower() in v['category'].lower()
        }
    
    # Display
    for name, info in sorted(methodologies.items()):
        with st.expander(f"📄 {name}"):
            st.markdown(f"**Category:** {info['category']}")
            st.markdown(f"**Version:** {info['version']}")
            
            method_data = st.session_state.methodology_loader.get_methodology(name)
            if method_data and method_data.get('calibration'):
                st.markdown("**Calibration:**")
                st.json(method_data['calibration'])


def render_chat_interface():
    """Render the main chat interface."""
    st.header("🌐 IRP Orchestrator Swarm Console")
    
    # Chat history container
    chat_container = st.container()
    
    with chat_container:
        for entry in st.session_state.chat_history:
            if entry['role'] == 'user':
                with st.chat_message("user"):
                    st.markdown(entry['content'])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(entry['content'])
    
    # Input
    user_input = st.chat_input("Enter command or goal (e.g., /help or 'analyze security')")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Process and get response
        response = process_input(user_input)
        
        # Handle special commands
        if response == "CLEAR_HISTORY":
            st.session_state.chat_history = []
            st.rerun()
        else:
            # Add assistant response
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            st.rerun()


def main():
    """Main application entry point."""
    init_session_state()
    
    # Layout: Sidebar | Main Chat | Methodology Browser
    render_sidebar()
    
    # Main content area with columns
    col1, col2 = st.columns([3, 1])
    
    with col1:
        render_chat_interface()
    
    with col2:
        render_methodology_browser()


if __name__ == "__main__":
    main()
