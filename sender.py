import csv
import json
import time
import requests
from datetime import datetime
from typing import Dict, Any

def send_package(package: Dict[str, Any]) -> None:
    """Send packet to server"""
    try:
        response = requests.post(
            "http://server:5000/api/packages",
            json=package,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        print(f"Sent package from {package['ip']}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send package: {e}")

def read_and_send_packages(csv_file: str) -> None:
    """Read CSV file and send packets according to timestamps"""
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        previous_timestamp = None
        
        for row in reader:

            unix_timestamp = int(row['Timestamp'])

            current_timestamp = datetime.fromtimestamp(unix_timestamp)
            
            if previous_timestamp is not None:
                delay = (current_timestamp - previous_timestamp).total_seconds()
                time.sleep(delay)
            
            package = {
                'ip': row['ip address'],
                'latitude': float(row['Latitude']),
                'longitude': float(row['Longitude']),
                'timestamp': current_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'suspicious': int(float(row['suspicious']))
            }
            
            send_package(package)
            previous_timestamp = current_timestamp

        # Send 'end letter'
        send_package({
            'ip': 'END_MARKER',
            'latitude': 0,
            'longitude': 0,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'suspicious': 0,
            'is_last': True
        })

    print("All packages sent.")
    sys.exit(0)    

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sender.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    print(f"Starting to send packages from {csv_file}")
    read_and_send_packages(csv_file)