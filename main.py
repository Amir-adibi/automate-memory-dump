import os
import subprocess
import sys
from dotenv import load_dotenv
from VM import VM


if __name__ == '__main__':
    vmrun_path = os.getenv('VMRUN_PATH')
    vmx_path = os.getenv('VMX_PATH')

    vm = VM(vmrun_path, vmx_path)

    # Start the VM
    print("Starting the virtual machine...")
