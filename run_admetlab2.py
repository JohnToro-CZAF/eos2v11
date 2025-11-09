import sys
import json
import pathlib
import requests


def main():
    """Run ADMETLab2 predictions via local Ersilia microservice.

    Usage: python run_admetlab2.py <smiles_or_input_file> <output_json>
    The first argument can be a SMILES string or a path to a file containing
    a SMILES string or SDF content.  The script posts the compound to the
    local Ersilia service (running at http://127.0.0.1:5000/predict) and
    writes the JSON response to the specified output file.
    """
    if len(sys.argv) < 3:
        print("Usage: python run_admetlab2.py <smiles_or_file> <output_json>")
        sys.exit(1)

    input_arg = sys.argv[1]
    output_path = pathlib.Path(sys.argv[2])

    # Determine if input is a file path or direct SMILES string
    input_path = pathlib.Path(input_arg)
    if input_path.exists() and input_path.is_file():
        compound_str = input_path.read_text().strip()
    else:
        compound_str = input_arg.strip()

    if not compound_str:
        print("Error: input compound is empty")
        sys.exit(1)

    # Prepare request to local Ersilia microservice
    url = "http://127.0.0.1:5000/run"
    payload = {"compound": compound_str}

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
    except Exception as exc:
        print(f"Error calling ADMETLab2 service: {exc}")
        sys.exit(2)

    # Write JSON output
    try:
        output_path.write_text(json.dumps(result, indent=2))
        print(f"Results written to {output_path}")
    except Exception as exc:
        print(f"Error writing output file: {exc}")
        sys.exit(3)


if __name__ == "__main__":
    main()
