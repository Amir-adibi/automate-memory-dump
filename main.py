import os
import subprocess
import sys

# Path to vmrun executable
vmrun = r'"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"'  # Modify this to your vmrun path

# Map the name of the VM to the .vmx file
vmx_map = {
    'Windows10': r'"C:\Users\Amir\Documents\Virtual Machines\Windows 10 x64\Windows 10 x64.vmx"'  # Modify this to your VM's .vmx file path
}

# Operation mappings for vmrun
operation_map = {
    'start': r' -T ws start ',
    'stop': r' -T ws stop ',
}


def operate_vm(host, operation):
    """
    This function performs operations on the virtual machine like starting and stopping.
    """
    if host not in vmx_map:
        print(f"Error: Host '{host}' does not exist!")
        sys.exit(1)

    if operation not in operation_map:
        print(f"Error: Operation '{operation}' is invalid!")
        sys.exit(1)

    cmd = vmrun + operation_map[operation] + vmx_map[host]
    print(f"Executing: {cmd}")
    subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    # Name of the VM (must be in vmx_map)
    host = 'Windows10'  # Modify this to the name you are using in vmx_map

    # Start the VM
    print("Starting the virtual machine...")
    operate_vm(host, 'start')
