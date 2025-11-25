import os
import re

def extract_personas_from_directory(directory_path, recursive=True):
    """
    Scans all files in a given directory to extract and catalogue
    potential persona or protocol definitions from raw chat logs.

    Args:
        directory_path (str): The path to the directory containing log files.
        recursive (bool): Whether to scan subdirectories recursively.

    Returns:
        dict: A dictionary where keys are filenames and values are lists of
              extracted persona strings.
    """
    # Regex to find explicit persona blocks marked by <persona>, <protocol>, <gem>, etc.
    persona_pattern = re.compile(
        r"""
        <(persona|protocol|gem|system_instruction|persona_definition)> # Start tag
        (.*?)                                                          # Content (non-greedy)
        </\1>                                                          # Matching end tag
        """,
        re.VERBOSE | re.IGNORECASE | re.DOTALL
    )

    # A more generic pattern for XML-style blocks like <tp:transmissionPacket>
    xml_block_pattern = re.compile(
        r"""
        <([a-zA-Z0-9_:]+)[^>]*>  # Match any opening XML-like tag
        (.*?)                   # Capture all content within
        </\1>                   # Match the corresponding closing tag
        """,
        re.VERBOSE | re.DOTALL
    )

    catalogued_personas = {}

    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at '{directory_path}'")
        return catalogued_personas

    print(f"Scanning directory: {directory_path}\n")

    if recursive:
        # Walk through all subdirectories
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                process_file(file_path, filename, persona_pattern, xml_block_pattern, catalogued_personas)
    else:
        # Only scan top-level files
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                process_file(file_path, filename, persona_pattern, xml_block_pattern, catalogued_personas)

    return catalogued_personas

def process_file(file_path, filename, persona_pattern, xml_block_pattern, catalogued_personas):
    """Process a single file to extract personas."""
    # Skip binary files and large files
    try:
        file_size = os.path.getsize(file_path)
        if file_size > 10 * 1024 * 1024:  # Skip files larger than 10MB
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # Find matches using both patterns
            explicit_matches = persona_pattern.findall(content)
            generic_matches = xml_block_pattern.findall(content)

            found_personas = []

            # Add explicitly tagged personas
            if explicit_matches:
                for match in explicit_matches:
                    # match[1] is the captured group with the persona content
                    found_personas.append(match[1].strip())

            # Add generic XML blocks if they seem relevant
            if generic_matches:
                for match in generic_matches:
                    # Add a check to only include substantial blocks of text
                    if len(match[1].strip()) > 200:  # Filter out small, irrelevant tags
                        # We re-add the tags here for context
                        full_block = f"<{match[0]}>{match[1].strip()}</{match[0]}>"
                        found_personas.append(full_block)

            if found_personas:
                catalogued_personas[file_path] = found_personas
                print(f"--- Found {len(found_personas)} potential persona(s) in: {file_path} ---")
    except (UnicodeDecodeError, PermissionError):
        # Skip binary files or files we can't read
        pass
    except Exception as e:
        print(f"Could not read or process file {file_path}: {e}")

# --- HOW TO USE ---

# 1. Set the path to the directory containing your chat logs.
log_directory = r'E:\8-16025DESKTOP DUMP'

# 2. Run the function
print("Starting persona extraction (recursive scan)...\n")
extracted_data = extract_personas_from_directory(log_directory, recursive=True)

# 3. Print the results
print("\n\n--- EXTRACTION COMPLETE ---\n")
if extracted_data:
    print(f"Total files with personas found: {len(extracted_data)}\n")
    for filepath, personas in extracted_data.items():
        print(f"File: {filepath}")
        for i, persona in enumerate(personas, 1):
            print(f"  Persona #{i} (length: {len(persona)} chars):")
            # Show first 500 characters of each persona
            preview = persona[:500]
            print("\n".join([f"    {line}" for line in preview.split('\n')]))
            if len(persona) > 500:
                print(f"    ... (truncated, full length: {len(persona)} chars)")
            print("-" * 60)
        print("=" * 80)
else:
    print("No potential personas found in the specified directory.")

# Save results to a file
output_file = r'E:\persona_extraction_results.txt'
with open(output_file, 'w', encoding='utf-8') as out:
    out.write(f"Persona Extraction Results\n")
    out.write(f"Scanned Directory: {log_directory}\n")
    out.write(f"{'=' * 80}\n\n")

    if extracted_data:
        out.write(f"Total files with personas found: {len(extracted_data)}\n\n")
        for filepath, personas in extracted_data.items():
            out.write(f"File: {filepath}\n")
            for i, persona in enumerate(personas, 1):
                out.write(f"\nPersona #{i}:\n")
                out.write("-" * 60 + "\n")
                out.write(persona)
                out.write("\n" + "-" * 60 + "\n")
            out.write("\n" + "=" * 80 + "\n\n")
    else:
        out.write("No potential personas found.\n")

print(f"\n\nFull results saved to: {output_file}")
