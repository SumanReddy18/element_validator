# URL Element Validator

This tool validates if specific HTML elements exist on given URLs.

## Setup

1. Install requirements:

```bash
chmod +x setup_env.sh  
./setup_env.sh  
pip install -r requirements.txt
```

2. Make sure you have Chrome browser installed.

## Usage

Run the validator with your CSV file:

### Validate All URLs
```bash
python url_validator.py your_file.csv
```

### Re-run Failed Cases
To re-validate only the rows marked as "FAIL" in the previous run:
```bash
python url_validator.py your_file.csv --rerun-failed
```

## Input CSV Format

The CSV file should have two columns:

- `url`: The website URL to check.
- `target_node`: The CSS selector to validate.

### Example:
```csv
url,target_node
https://example.com,.example-class
https://another-example.com,#example-id
```

## Output

Results will be saved in a new file with the suffix `_validation` added to the original file name. The output will include the following columns:

- `status`: PASS/FAIL/ERROR.
- `error_message`: Detailed error message if validation fails.

### Status Explanation:
- **PASS**: The element was found and is interactable.
- **FAIL**: The element was not found or is not interactable.
- **ERROR**: A technical issue occurred (e.g., invalid selector, network error).

## Logs

Logs will be printed to the console during execution, providing detailed information about the validation process.