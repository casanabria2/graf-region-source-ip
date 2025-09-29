# Grafana Region Source IP Filter

A Python script that filters Grafana source IPs against AWS region ranges, helping you identify which Grafana IPs are located in specific AWS regions.

## Overview

This tool downloads the current list of Grafana source IPs and compares them against AWS IP ranges for a specified region. It's useful for:
- Network security analysis
- Understanding Grafana's infrastructure distribution
- AWS region-specific IP filtering
- Network troubleshooting and monitoring

## Features

- 🌐 **AWS Region Filtering** - Filter IPs by specific AWS regions
- 🔍 **IPv6 Support** - Optional IPv6 address inclusion
- 📊 **CIDR Range Output** - Shows which AWS subnet each IP belongs to
- 🛠️ **VS Code Debugging** - Pre-configured debug configurations
- ⚡ **Fast Processing** - Efficient IP range checking using Python's ipaddress module
- 🎯 **Precise Matching** - Accurate CIDR range matching

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/casanabria2/graf-region-source-ip.git
   cd graf-region-source-ip
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
# Filter IPs for us-west-2 (default region)
python filter_region.py

# Filter IPs for a specific region
python filter_region.py --region us-east-1

# Include IPv6 addresses
python filter_region.py --region us-west-2 --include-ipv6

# Show help and all options
python filter_region.py --help
```

### Command Line Options

- `--region REGION` - AWS region to filter by (default: us-west-2)
- `--include-ipv6` - Include IPv6 addresses in the source IP list
- `--help` - Show help message and exit

### Example Output

```
Fetching AWS ranges for region: us-west-2...
Fetching Grafana source IPs...
Matching IPs:
52.24.218.184 -> 52.24.0.0/14
54.191.255.86 -> 54.184.0.0/13
```

## Development

### VS Code Debugging

The repository includes pre-configured VS Code debug configurations:

1. **"Debug Filter Region Script"** - Debug with default settings
2. **"Debug Filter Region Script (with IPv6)"** - Debug with IPv6 support
3. **"Python Debugger: Current File"** - Debug any Python file

To debug:
1. Open the project in VS Code
2. Set breakpoints in `filter_region.py`
3. Press F5 or use the Run and Debug panel
4. Select a debug configuration

### Project Structure

```
graf-region-source-ip/
├── filter_region.py      # Main Python script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .vscode/             # VS Code configuration
│   ├── launch.json      # Debug configurations
│   └── settings.json    # Python interpreter settings
└── venv/                # Virtual environment (created locally)
```

## How It Works

1. **Download AWS Ranges**: Fetches current AWS IP ranges from `https://ip-ranges.amazonaws.com/ip-ranges.json`
2. **Filter by Region**: Extracts only the IP ranges for the specified AWS region
3. **Download Source IPs**: Fetches Grafana source IPs from `https://grafana.com/api/hosted-grafana/source-ips.txt`
4. **IP Matching**: Checks each source IP against the AWS region ranges using CIDR matching
5. **Output Results**: Displays matching IPs with their corresponding AWS subnet ranges

## Requirements

- `requests>=2.25.0` - HTTP library for downloading data

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
