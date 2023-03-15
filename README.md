
# Configure Multiple Cisco Switches with Netmiko

This Python script uses the Netmiko library to configure multiple Cisco switches via SSH. Specifically, the script logs in to each switch in a list of IP addresses provided in a text file, enters the commands to create a standard access-list, permits a specific IP address, saves the configuration, and logs out.

The script utilizes multithreading to connect to multiple switches at the same time, improving performance and reducing the time required to complete the configuration.

## Requirements

-   Python 3.x
-   Netmiko library (`pip install netmiko`)
-   A text file containing a list of switch IP addresses, one per line.

## Usage

1.  Clone this repository to your local machine, or download the script file (`configure_switches.py`) directly.
2.  Install the Netmiko library by running `pip install netmiko` in a terminal window.
3.  Create a text file containing a list of switch IP addresses, one per line. For example:
    
    Copy code
        `192.168.1.1`
        
    `192.168.1.2`
    
    `192.168.1.3`
    

4.  Update the script with your device type, command set, and credentials. Specifically, modify the following variables:
    -   `device_type`: The device type of the switches. See [Netmiko's supported devices](https://github.com/ktbyers/netmiko/blob/develop/PLATFORMS.md) for a list of supported device types.
    -   `command_set`: The list of commands to execute on each switch. Add or remove commands as needed.
    -   `username`: The username to use when connecting to the switches.
    -   `password`: The password to use when connecting to the switches.
5.  Run the script by executing `python configure_switches.py` in a terminal window. The script will connect to each switch in the IP address list, execute the commands, and log out.
6.  After the script completes, it will display the number of successful and failed connections, as well as the IP addresses of the switches that had errors.

## Troubleshooting

If you encounter any errors while running the script, ensure that:

-   The switch IP addresses in the text file are correct and accessible from your network.
-   Your device type and command set are correct for the switches you are configuring.
-   Your username and password are correct for accessing the switches.
-   You have installed the Netmiko library (`pip install netmiko`) and imported it in your Python script.
