#!/usr/bin/env python3
"""
Filter Grafana IPs against AWS region ranges
Usage: python filter_region.py [--region REGION] [--include-ipv6]
Example: python filter_region.py --region us-east-1 --include-ipv6
"""

import argparse
import json
import re
import requests
import ipaddress
import sys
from typing import List, Set, Tuple


def download_aws_ranges(region: str) -> List[str]:
    """Download AWS IP ranges for the specified region."""
    aws_url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    print(f"Fetching AWS ranges for region: {region}...", file=sys.stderr)
    
    try:
        response = requests.get(aws_url)
        response.raise_for_status()
        data = response.json()
        
        ranges = []
        # Add IPv4 prefixes
        for prefix in data.get('prefixes', []):
            if prefix.get('region') == region:
                ranges.append(prefix.get('ip_prefix'))
        
        # Add IPv6 prefixes
        for prefix in data.get('ipv6_prefixes', []):
            if prefix.get('region') == region:
                ranges.append(prefix.get('ipv6_prefix'))
        
        return [r for r in ranges if r]  # Filter out None values
        
    except requests.RequestException as e:
        print(f"Error downloading AWS ranges: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing AWS ranges JSON: {e}", file=sys.stderr)
        sys.exit(1)


def download_source_ips(include_ipv6: bool = False) -> List[str]:
    """Download Grafana source IPs."""
    source_url = "https://grafana.com/api/hosted-grafana/source-ips.txt"
    print("Fetching Grafana source IPs...", file=sys.stderr)
    
    try:
        response = requests.get(source_url)
        response.raise_for_status()
        content = response.text
        
        # Extract IPs using regex
        ipv4_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ipv6_pattern = r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b|::1|::'
        
        ips = []
        ips.extend(re.findall(ipv4_pattern, content))
        
        if include_ipv6:
            ips.extend(re.findall(ipv6_pattern, content))
        
        return ips
        
    except requests.RequestException as e:
        print(f"Error downloading source IPs: {e}", file=sys.stderr)
        sys.exit(1)


def ip_in_cidr(ip: str, cidr: str) -> bool:
    """Check if an IP address is within a CIDR range."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        network = ipaddress.ip_network(cidr, strict=False)
        return ip_obj in network
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        return False


def find_matching_ips(source_ips: List[str], aws_ranges: List[str]) -> List[Tuple[str, str]]:
    """Find source IPs that match any AWS region range.
    
    Returns:
        List of tuples containing (ip, cidr) for matching IPs
    """
    matching_ips = []
    
    print("Matching IPs:", file=sys.stderr)
    for ip in source_ips:
        for cidr in aws_ranges:
            if ip_in_cidr(ip, cidr):
                matching_ips.append((ip, cidr))
                break
    
    return matching_ips


def main():
    parser = argparse.ArgumentParser(
        description="Filter Grafana IPs against AWS region ranges",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python filter_region.py --region us-east-1
  python filter_region.py --region us-west-2 --include-ipv6
  python filter_region.py --region eu-west-1 --include-ipv6
        """
    )
    
    parser.add_argument(
        '--region',
        default='us-west-2',
        help='AWS region to filter by (default: us-west-2)'
    )
    
    parser.add_argument(
        '--include-ipv6',
        action='store_true',
        help='Include IPv6 addresses in the source IP list'
    )
    
    args = parser.parse_args()
    
    # Download AWS ranges for the specified region
    aws_ranges = download_aws_ranges(args.region)
    
    if not aws_ranges:
        print(f"No AWS ranges found for region: {args.region}", file=sys.stderr)
        sys.exit(1)
    
    # Download source IPs
    source_ips = download_source_ips(args.include_ipv6)
    
    if not source_ips:
        print("No source IPs found", file=sys.stderr)
        sys.exit(1)
    
    # Find matching IPs
    matching_ips = find_matching_ips(source_ips, aws_ranges)
    
    # Output matching IPs with their CIDR ranges
    for ip, cidr in matching_ips:
        print(f"{ip} -> {cidr}")


if __name__ == "__main__":
    main()
