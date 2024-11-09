import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

DEFAULT_PORTS = range(1, 1001)


def port_scanning(target, port):
  """Attempts to connect to the specified port on the target"""
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
      soc.settimeout(1)
      result = soc.connect_ex((target, port))
      if result == 0:
        print(f"Port {port} open")
  except Exception as e:
    print(f"Error scanning port: {e}")


def resolve_domain(target):
  """Resolves the domain name to an IP address"""
  try:
    domain = socket.gethostbyname(target)
    return domain
  except socket.gaierror:
    print(f"Can't resolve domain: {target}")
    return None


def parse_port_range(port_range_input):
  """Parses a port range string (e.g 20,80-84) to return a list of ports"""
  port_list = []
  for range_port in port_range_input.split(","):
    if "-" in range_port:
      start_port, end_port = map(int, range_port.split("-"))
      port_list.extend(range(start_port, end_port+1))
    else:
      port_list.append(int(range_port))
  return port_list


def main():
  parser = argparse.ArgumentParser(description="Simple Port Scanning")
  parser.add_argument("--domain", "-d", required=True, help="Target domain or IP address")
  parser.add_argument("--ports", "-p", help="Ports range e.g., '20,35-40' (default: 1-1000)")

  args = parser.parse_args()

  target = resolve_domain(target=args.domain)
  if not target:
    return

  # Determin port range (either using spesific port or default)
  port_range = parse_port_range(args.ports) if args.ports else DEFAULT_PORTS

  # Perform port scanning using multithreading
  with ThreadPoolExecutor(max_workers=100) as executor:
    for port in port_range:
      executor.submit(port_scanning, target, port)
  print("Scanning Finished!")


if __name__=="__main__":
  main()
