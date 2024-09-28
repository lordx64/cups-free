# CUPS Removal Script

A Python script to completely remove CUPS (Common Unix Printing System) and associated services from Linux systems.

## Features

- Removes CUPS installations from both APT and Snap
- Stops and disables CUPS-related systemd services
- Cleans up residual files and directories
- Handles errors gracefully to ensure complete removal

## Components Affected

### Services Stopped and Disabled
- cups.service
- cups.socket
- cups.path
- cups-browsed.service
- cups-proxyd.service

### APT Packages Removed
- cups
- cups-bsd
- cups-client
- cups-common
- cups-core-drivers
- cups-daemon
- cups-filters
- cups-filters-core-drivers
- cups-ppdc
- cups-server-common
- cups-browsed

### Snap Packages Removed
- cups
- cups-browsed
- cups-proxyd

### Directories and Files Cleaned
- /etc/cups/
- /var/spool/cups/
- /var/cache/cups/
- /var/log/cups/
- /var/lib/cups/
- /var/snap/cups/

## Prerequisites

- Python 3
- Root privileges
- Linux system with systemd

## Installation

1. Clone this repository or download the `cups.py` script.
2. Make the script executable:
   ```bash
   chmod +x cups-free.py
   ```

## Usage

Run the script as root:

  ```bash
   sudo ./cups-free.py
   ```

## What Happens When You Run the Script?

- Systemd Services: The script checks if each CUPS-related service is active and only attempts to stop or disable it if it is running. If a service is already inactive or not loaded, the script skips the action without errors.
- APT Packages: The script removes all CUPS-related packages installed via APT and cleans up dependencies using apt-get autoremove.
- Snap Packages: The script removes CUPS and its associated Snap packages if installed.
- File Cleanup: It deletes all remaining files and directories related to CUPS, ensuring no residual configuration or data remains.

## Error Handling

The script includes robust error handling:
- Continues execution if services are not active or loaded
- Logs errors during package removal or file deletion without stopping
- Gracefully handles missing Snap packages

## Warning

This script will completely remove CUPS and all associated components. Ensure you don't need printing services before running it.

## Troubleshooting

- Check terminal output for any error messages
- Ensure an active internet connection for package removal
- If a specific component fails to remove, you can manually remove it using the appropriate system commands

## Contributing

Contributions to improve the script are welcome. Please submit a pull request or open an issue to discuss proposed changes.

## License

This script is open-source and available under the MIT license. Feel free to modify and distribute it as needed.
