# SSH Configuration Script

This Python script automates the process of configuring multiple Cisco IOS devices over SSH. It uses the `netmiko` library for SSH connections, `concurrent.futures` for parallel execution, and `colorama` for colored output. The script reads device IPs from a file, prompts the user for SSH credentials, and applies a predefined set of commands to each device.

## Features

- Parallel execution of SSH connections using thread pooling.
- Logging of success and error messages.
- Color-coded output for better readability.
- Secure credential input using `getpass`.

## Requirements

- Python 3.x
- `netmiko` library
- `colorama` library

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/saeed205/Configure-Multiple-Cisco-Switches.git
   cd Configure-Multiple-Cisco-Switches
   ```

2. Install the required Python packages:
   ```sh
   pip install netmiko colorama
   ```

3. Create a file named `switch_list.txt` in the same directory, and list the IP addresses of the devices to be configured, one per line.

## Usage

1. Run the script:
   ```sh
   python configure_switches.py
   ```

2. Enter your SSH username when prompted.
3. Enter your SSH password when prompted.

## Example Output

```
Enter your SSH username: admin
Enter your SSH password: 
2023-07-07 10:00:00 - INFO - Successfully configured 192.168.1.1:
ip access-list standard Cisco
permit 192.168.1.10
end
wr
✅
2023-07-07 10:00:02 - ERROR - Error configuring 192.168.1.2: Authentication failed. ❌
...

Successful connections: 1 ✅
Failed connections: 1 ❌
IP addresses of failed connections:
192.168.1.2
```

## Script Details

### Initialization

- **Colorama** is initialized to support colored terminal output.
- **Logging** is configured to provide timestamped log messages.

### Device Configuration

The script defines a command set to be executed on each device:
```python
command_set = ['ip access-list standard Cisco', 'permit 192.168.1.10', 'end', 'wr']
```

### Credentials

The script securely prompts for SSH credentials using `getpass`:
```python
username = input(Style.BRIGHT + Fore.CYAN + 'Enter your SSH username: ')
password = getpass.getpass(Style.BRIGHT + Fore.CYAN + 'Enter your SSH password: ')
```

### SSH Connection Handling

The `ssh_connect` function manages the SSH connection to each device, executes the commands, and logs the results:
```python
def ssh_connect(device_ip):
    ...
    try:
        net_connect = ConnectHandler(**device)
        output = net_connect.send_config_set(command_set)
        logger.info(Fore.GREEN + f'Successfully configured {device_ip}:\n{output} ✅')
        return True, device_ip
    except Exception as e:
        logger.error(Fore.RED + f'Error configuring {device_ip}: {e} ❌')
        return False, device_ip
    finally:
        net_connect.disconnect()
```

### Thread Pool Execution

A thread pool is created to handle multiple SSH connections concurrently:
```python
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_ip = {executor.submit(ssh_connect, switch_ip): switch_ip for switch_ip in switch_list}
```

### Result Collection

The script collects the results of the SSH connections and logs the summary:
```python
for future in concurrent.futures.as_completed(future_to_ip):
    success, ip = future.result()
    if success:
        success_count += 1
    else:
        fail_count += 1
        failed_ips.append(ip)
```

## License

This project is licensed under the MIT License.
