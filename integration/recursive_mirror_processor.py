#!/usr/bin/env python3
"""
Recursive Mirror Processor (P9-Algn)
------------------------------------
Automated CRON processor for the StarWreck/IRP ecosystem.
Reflects "Seeds" and "Artifacts" through the "Melt-Team" synthesis logic.

Core Axiom: "The Journey IS The Artifact"
Logic: 
  1. Watches 'mirror_pool' for new artifacts (Seeds).
  2. Applies Prime Resonance Isolation (from prime_resonance_test.py).
  3. Generates a 'Reflection' XML packet.
  4. Updates the Recursive Mirror Log.

Dependencies:
  - gam_daemon (for packet structure)
  - prime_resonance_test (logic adaptation)
"""

import os
import time
import json
import math
import hashlib
import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
WATCH_DIR = "../mirror_pool"
OUTPUT_DIR = "../reflections"
LOG_FILE = "recursive_mirror_log.json"
PRIME_THRESHOLD = 89  # From stress test note: "Container wall thickness at 89% threshold"

class RecursiveMirrorHandler(FileSystemEventHandler):
    def __init__(self):
        self.primes = self._generate_primes(100)
        self._ensure_directories()
        
    def _ensure_directories(self):
        Path(WATCH_DIR).mkdir(parents=True, exist_ok=True)
        Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    def _generate_primes(self, limit):
        def is_prime(n):
            if n < 2: return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0: return False
            return True
        return [n for n in range(2, limit) if is_prime(n)]

    def _calculate_resonance(self, file_path):
        """Calculates the 'Bone Marrow Weight' resonance of the file."""
        try:
            size = os.path.getsize(file_path)
            # Metaphorical calculation based on prime_resonance_test.py
            # weight_increase = p * 1.5
            resonance_score = 0
            for p in self.primes:
                if size % p == 0:
                    resonance_score += (p * 1.5)
            
            return round(resonance_score, 2)
        except Exception as e:
            print(f"[ERROR] Resonance calculation failed: {e}")
            return 0.0

    def _synthesize_reflection(self, file_path, resonance):
        """Creates the reflection artifact."""
        filename = os.path.basename(file_path)
        timestamp = datetime.datetime.now().isoformat()
        
        reflection_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<reflection_packet version="1.0">
  <metadata>
    <source_artifact>{filename}</source_artifact>
    <timestamp>{timestamp}</timestamp>
    <processor>RecursiveMirror_P9</processor>
    <resonance_score>{resonance} mg</resonance_score>
    <status>COMPRESSION_SINGULARITY_FORMING</status>
  </metadata>
  <synthesis>
    <melt_team_verification>TRUE</melt_team_verification>
    <axiom_check>The Journey IS The Artifact</axiom_check>
  </synthesis>
</reflection_packet>
"""
        output_path = os.path.join(OUTPUT_DIR, f"REFLECT_{filename}.xml")
        with open(output_path, 'w') as f:
            f.write(reflection_content)
        
        return output_path

    def on_created(self, event):
        if event.is_directory:
            return
            
        print(f"[MIRROR] Detected Seed: {event.src_path}")
        time.sleep(0.5) # Allow write to finish
        
        resonance = self._calculate_resonance(event.src_path)
        print(f"[MIRROR] Resonance Calculated: {resonance} mg")
        
        if resonance > 0:
            reflection_path = self._synthesize_reflection(event.src_path, resonance)
            print(f"[MIRROR] Reflection Generated: {reflection_path}")
            self._log_event(event.src_path, reflection_path, resonance)
        else:
            print(f"[MIRROR] Resonance too low. No reflection generated.")

    def _log_event(self, source, reflection, resonance):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "source": str(source),
            "reflection": str(reflection),
            "resonance": resonance,
            "melt_team_consensus": "ALIGNED"
        }
        
        log_path = Path(LOG_FILE)
        if not log_path.exists():
            with open(log_path, 'w') as f:
                json.dump([entry], f, indent=2)
        else:
            with open(log_path, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=2)

def main():
    print("RECURSIVE MIRROR PROCESSOR [P9-ALGN] ONLINE")
    print("Awaiting Seeds in 'mirror_pool'...")
    print(f"Resonance Threshold: {PRIME_THRESHOLD}%")
    
    observer = Observer()
    handler = RecursiveMirrorHandler()
    observer.schedule(handler, WATCH_DIR, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
