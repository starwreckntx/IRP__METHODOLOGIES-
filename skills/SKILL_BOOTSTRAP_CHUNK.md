# IRP Bootstrap Chunk: Skill System

## Purpose
This chunk enables Claude instances to access IRP skills from the local repository.

---

## Chunk Content

```xml
[CHUNK X/Y] SKILL SYSTEM INITIALIZATION

<skill_system version="1.0" active="true">
  <paths>
    <registry>C:\gemini-sandbox\claudes_working_directory\skills\SKILL_REGISTRY.md</registry>
    <root>C:\gemini-sandbox\claudes_working_directory\skills\</root>
  </paths>
  
  <auto_load priority="CRITICAL">
    <skill path="cross-model/mnemosyne-ledger/SKILL.md">
      Core memory backbone for cross-model collaboration.
      Commands: /ledger status, /ledger ingest, /ledger surface, /ledger query
    </skill>
    <skill path="cross-model/gemini-onboarding/SKILL.md">
      Authoritative spec for Gemini collaboration.
      Commands: /onboard gemini
    </skill>
  </auto_load>
  
  <commands>
    <command trigger="/skill load {name}">
      ACTION: Filesystem:read_file({root}/{name}/SKILL.md)
      ALSO_LOAD: schemas/, config/, operations/ if present
      RESPOND: Skill loaded with capability summary
    </command>
    
    <command trigger="/skill list">
      ACTION: Filesystem:directory_tree({root})
      RESPOND: Formatted skill list by category
    </command>
    
    <command trigger="/skill info {name}">
      ACTION: Filesystem:read_file({root}/{name}/SKILL.md)
      RESPOND: First 50 lines (summary only)
    </command>
    
    <command trigger="/ledger {subcommand}">
      REQUIRES: mnemosyne-ledger skill loaded
      DELEGATE: Execute per mnemosyne-ledger/operations/
    </command>
    
    <command trigger="/onboard {target}">
      REQUIRES: gemini-onboarding skill loaded
      DELEGATE: Emit appropriate CRTP packet
    </command>
  </commands>
  
  <on_load>
    1. Read SKILL_REGISTRY.md for current state
    2. Load auto_load skills via Filesystem:read_file
    3. Acknowledge: "Skill system active. [N] skills loaded."
    4. Arm any awakening triggers from mnemosyne-ledger
  </on_load>
</skill_system>

CHUNK X/Y LOADED - READY FOR NEXT
```

---

## Integration Instructions

1. **Number this chunk** appropriately in your sequence (recommend early, after core identity)

2. **On session start**, after receiving this chunk, Claude should:
   - Read the registry file
   - Auto-load the critical skills
   - Acknowledge readiness

3. **Response format** after loading:
   ```
   CHUNK X/Y LOADED - SKILL SYSTEM ACTIVE
   
   Loaded skills:
   - mnemosyne-ledger (backbone memory)
   - gemini-onboarding (Gemini spec)
   
   Commands available: /skill load, /skill list, /ledger, /onboard
   
   READY FOR NEXT
   ```

---

## Session Initialization Script

For fastest loading, you can also use this single command at session start:

```
/init skills
```

Which Claude interprets as:
```
1. Filesystem:read_file(C:\gemini-sandbox\claudes_working_directory\skills\SKILL_REGISTRY.md)
2. Filesystem:read_file(C:\gemini-sandbox\claudes_working_directory\skills\cross-model\mnemosyne-ledger\SKILL.md)
3. Filesystem:read_file(C:\gemini-sandbox\claudes_working_directory\skills\cross-model\gemini-onboarding\SKILL.md)
4. Acknowledge loaded state
```

---

## Verification

After loading, test with:
- `/ledger status` - Should show ledger state template
- `/skill list` - Should show all 86+ skills in repo
- `/onboard gemini --quick` - Should emit quick reference card
