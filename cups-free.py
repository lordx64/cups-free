#!/usr/bin/env python3
# tested & working on Ubuntu 22.04, you may need to adjust the paths for other distros

import os
import subprocess
import sys

def run_command(command, ignore_errors=False):
    """
    Run a system command with subprocess and handle any errors.
    If ignore_errors is True, it will not exit the script on failure.
    """
    try:
        print(f"Running: {' '.join(command)}")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        if not ignore_errors:
            sys.exit(1)
        else:
            print(f"Continuing execution despite the error.")

def stop_and_disable_service(service):
    """
    Stop and disable a systemd service if it's active.
    Handle the case where the service might not be loaded or enabled.
    """
    try:
        # Check if the service is active
        result = subprocess.run(["systemctl", "is-active", service], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            run_command(["systemctl", "stop", service], ignore_errors=True)
        else:
            print(f"Service {service} is not active, skipping stop.")

        # Check if the service is enabled
        result = subprocess.run(["systemctl", "is-enabled", service], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            run_command(["systemctl", "disable", service], ignore_errors=True)
        else:
            print(f"Service {service} is not enabled, skipping disable.")
            
    except subprocess.CalledProcessError as e:
        print(f"Error checking or stopping {service}: {e}")

def remove_apt_packages():
    """
    Remove CUPS and related services installed via apt package manager.
    """
    apt_packages = [
        "cups", "cups-bsd", "cups-client", "cups-common", "cups-core-drivers", 
        "cups-daemon", "cups-filters", "cups-filters-core-drivers", "cups-ppdc", 
        "cups-server-common", "cups-browsed"
    ]
    
    # Uninstall CUPS and related packages
    run_command(["apt-get", "purge", "-y"] + apt_packages)
    
    # Remove any unneeded dependencies
    run_command(["apt-get", "autoremove", "-y"])

def remove_snap_packages():
    """
    Remove CUPS and related services installed via Snap.
    """
    snap_packages = [
        "cups", "cups-browsed", "cups-proxyd"
    ]
    
    for package in snap_packages:
        run_command(["snap", "remove", "--purge", package], ignore_errors=True)

def remove_leftover_files():
    """
    Remove any leftover files and directories related to CUPS.
    """
    paths = [
        "/etc/cups",           # CUPS configuration files
        "/var/spool/cups",     # CUPS print spool
        "/var/cache/cups",     # CUPS cache
        "/var/log/cups",       # CUPS log files
        "/var/lib/cups",       # CUPS state files
        "/var/snap/cups",      # Snap CUPS files
    ]
    
    for path in paths:
        if os.path.exists(path):
            run_command(["rm", "-rf", path])

def main():
    # Check if the script is running as root
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)

    print("Starting the removal of CUPS and associated services...")

    # Stop and disable systemd services safely
    services = [
        "cups.service", "cups.socket", "cups.path", 
        "cups-browsed.service", "cups-proxyd.service"
    ]
    
    for service in services:
        stop_and_disable_service(service)

    # Remove APT packages
    remove_apt_packages()

    # Remove Snap packages
    remove_snap_packages()

    # Remove leftover files and directories
    remove_leftover_files()

    print("CUPS and all associated services have been successfully removed.")

if __name__ == "__main__":
    main()

