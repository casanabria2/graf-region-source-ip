#!/usr/bin/env bash
# Filter Grafana IPs against AWS region ranges
# Usage: ./filter_region.sh [region]
# Example: ./filter_region.sh us-east-1

REGION="${1:-us-west-2}"
AWS_URL="https://ip-ranges.amazonaws.com/ip-ranges.json"
SOURCE_URL="https://grafana.com/api/hosted-grafana/source-ips.txt"

# Download AWS ranges and filter by region
echo "Fetching AWS ranges for region: $REGION ..." >&2
AWS_RANGES=$(curl -s "$AWS_URL" | jq -r \
  --arg REGION "$REGION" '
    [.prefixes[]? | select(.region==$REGION) | .ip_prefix] +
    [.ipv6_prefixes[]? | select(.region==$REGION) | .ipv6_prefix] |
    .[]'
)

# Download Grafana source IPs
echo "Fetching Grafana source IPs..." >&2
SOURCE_IPS=$(curl -s "$SOURCE_URL" | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}|([0-9a-fA-F:]+:+)+[0-9a-fA-F]+')

# Check each source IP against region ranges
echo "Matching IPs:" >&2
for ip in $SOURCE_IPS; do
  for cidr in $AWS_RANGES; do
    if ipcalc -c "$ip" "$cidr" >/dev/null 2>&1; then
      echo "$ip"
      break
    fi
  done
done