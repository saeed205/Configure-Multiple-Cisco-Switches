from netmiko import ConnectHandler
import concurrent.futures

# Define the device type and command set for netmiko
device_type = 'cisco_ios'
command_set = ['ip access-list standard Cisco', 'permit 192.168.1.10', 'end', 'wr']

# Read the list of devices from a txt file
with open('switch_list.txt', 'r') as f:
    switch_list = f.read().splitlines()

# Create a list to store the SSH connections
connections = []

# Define counters for successful and failed connections
success_count = 0
fail_count = 0

# Define a function to handle SSH connections
def ssh_connect(device_ip):
    # Define the device credentials
    device = {
        'device_type': device_type,
        'ip': device_ip,
        'username': 'your_username',
        'password': 'your_password',
    }
    # Create a netmiko SSH connection to the device
    try:
        net_connect = ConnectHandler(**device)
        # Execute the commands
        output = net_connect.send_config_set(command_set)
        # Print the output for verification
        print(f'Successfully configured {device_ip}:\n{output}')
        return True
    except Exception as e:
        print(f'Error configuring {device_ip}: {e}')
        return False
    finally:
        net_connect.disconnect()

# Create a thread pool to handle the SSH connections
with concurrent.futures.ThreadPoolExecutor(max_workers=len(switch_list)) as executor:
    # Submit the SSH connections to the thread pool
    for switch_ip in switch_list:
        connections.append(executor.submit(ssh_connect, switch_ip))

# Wait for all connections to complete
for connection in concurrent.futures.as_completed(connections):
    # Increment the counters based on the results
    if connection.result():
        success_count += 1
    else:
        fail_count += 1

# Print the results
print(f'Successful connections: {success_count}')
print(f'Failed connections: {fail_count}')
if fail_count > 0:
    print('IP addresses of failed connections:')
    for connection in connections:
        if not connection.result():
            print(connection.args[0])
