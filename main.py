import os
import subprocess
import sys

from dotenv import load_dotenv
from VM import VM

if __name__ == '__main__':
    load_dotenv()
    vmrun_path = os.getenv('VMRUN_PATH')
    vmx_path = os.getenv('VMX_PATH')
    vm_dir = os.getenv('VM_DIR')

    vm = VM(vmrun_path, vmx_path, vm_dir)

    # Start the VM
    # print("Starting the virtual machine...")
    # vm.start_vm()

    vm.capture_initial_snapshot("clean_state", "C:\\Users\\Amir\\Desktop\\Git\\project\\automate-memory-dump\\snapshots")

