import logging
from netmiko import ConnectHandler
import concurrent.futures
import getpass
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the device type and command set for netmiko
device_type = 'cisco_ios'
command_set = ['ip access-list standard Cisco', 'permit 192.168.1.10', 'end', 'wr']

# Read the list of devices from a txt file
with open('switch_list.txt', 'r') as f:
    switch_list = f.read().splitlines()

# Get username and password from the user
username = input(Style.BRIGHT + Fore.CYAN + 'Enter your SSH username: ')
password = getpass.getpass(Style.BRIGHT + Fore.CYAN + 'Enter your SSH password: ')

# Define counters for successful and failed connections
success_count = 0
fail_count = 0
failed_ips = []

# Define a function to handle SSH connections
def ssh_connect(device_ip):
    # Define the device credentials
    device = {
        'device_type': device_type,
        'ip': device_ip,
        'username': username,
        'password': password,
    }
    # Create a netmiko SSH connection to the device
    try:
        net_connect = ConnectHandler(**device)
        # Execute the commands
        output = net_connect.send_config_set(command_set)
        # Log the output for verification
        logger.info(Fore.GREEN + f'Successfully configured {device_ip}:\n{output} ✅')
        return True, device_ip
    except Exception as e:
        logger.error(Fore.RED + f'Error configuring {device_ip}: {e} ❌')
        return False, device_ip
    finally:
        net_connect.disconnect()

# Create a thread pool to handle the SSH connections
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Submit the SSH connections to the thread pool
    future_to_ip = {executor.submit(ssh_connect, switch_ip): switch_ip for switch_ip in switch_list}

# Wait for all connections to complete and collect results
for future in concurrent.futures.as_completed(future_to_ip):
    success, ip = future.result()
    if success:
        success_count += 1
    else:
        fail_count += 1
        failed_ips.append(ip)

# Print the results with emojis and colors
logger.info(Style.BRIGHT + Fore.GREEN + f'Successful connections: {success_count} ✅')
logger.info(Style.BRIGHT + Fore.RED + f'Failed connections: {fail_count} ❌')
if fail_count > 0:
    logger.info(Style.BRIGHT + Fore.RED + 'IP addresses of failed connections:')
    for ip in failed_ips:
        logger.info(Fore.RED + ip)