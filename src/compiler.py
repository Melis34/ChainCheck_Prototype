import subprocess
import json
import sys

def parse_solidity(file_path):
    try:
        # Run solc to generate AST in JSON format
        result = subprocess.run(
            ["solc", "--ast-compact-json",  file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Print raw outputs for debugging
        # print("Raw STDOUT:", result.stdout)
        # print("STDERR:", result.stderr)

        # Check for errors
        if result.returncode != 0:
            print("Error executing solc:", result.stderr)
            return None

        # Preprocess the output to remove extra lines
        output_lines = result.stdout.splitlines()
        json_start_index = next((i for i, line in enumerate(output_lines) if line.startswith("{")), None)
        
        if json_start_index is None:
            print("Error: Could not find the start of JSON in solc output.")
            return None

        # Extract the JSON part
        json_output = "\n".join(output_lines[json_start_index:])
        
        # Parse the JSON output
        try:
            ast = json.loads(json_output)
        except json.JSONDecodeError as e:
            print("JSON parsing error:", e)
            # print("Preprocessed output was:", json_output)
            return None
        # print(ast)
        return ast

    except FileNotFoundError:
        print("Error: solc not found. Make sure it is installed and in your PATH.")
        sys.exit(1)
    except Exception as e:
        print("Unexpected error:", str(e))
        sys.exit(1)
