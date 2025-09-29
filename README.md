# Grafana Region Source IP Filter

This project contains scripts to filter Grafana source IPs against AWS region ranges.

## Files

- `graf-region-source-ip.sh` - Original bash script
- `filter_region.py` - Python equivalent with additional features
- `requirements.txt` - Python dependencies

## Python Script Usage

### Prerequisites

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Script

```bash
# Basic usage (default region: us-west-2)
python filter_region.py

# Specify a region
python filter_region.py --region us-east-1

# Include IPv6 addresses
python filter_region.py --region us-west-2 --include-ipv6

# Show help
python filter_region.py --help
```

### Features

- Downloads AWS IP ranges for the specified region
- Downloads Grafana source IPs
- Checks each source IP against AWS region ranges
- Optional IPv6 support
- Command-line argument parsing
- Error handling and informative output

### Output

The script outputs matching IP addresses to stdout, with progress information sent to stderr.
