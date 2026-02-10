"""
Allow running Context Mortality Audit CLI as a module:
    python -m irp_swarm_console.context_mortality <command> [options]
"""

from .cli import main

if __name__ == "__main__":
    main()
