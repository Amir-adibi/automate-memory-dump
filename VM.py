import sys
import os
import subprocess
import shutil
import time

# Automate Operations on a single VM
class VM:
    operation_map = {
        'start': r' -T ws start ',
        'stop': r' -T ws stop ',

        'createSnap': r' -T ws snapshot ',
        'revertSnap': r' -T ws revertToSnapshot ',
    }

    initial_snapshot_name: str
    base_vmem_file: str = None

    def __init__(self, vmrun_path: str, vmx_path: str, vm_dir: str):
        self.vmrun = self.trim_paths(vmrun_path)
        self.vmx = self.trim_paths(vmx_path)
        self.vm_dir = vm_dir

    def start_vm(self):
        cmd = self.vmrun + self.operation_map['start'] + self.vmx
        print(f"Executing: {cmd}")
        subprocess.run(cmd, shell=True)

    def stop_vm(self):
        cmd = self.vmrun + self.operation_map['stop'] + self.vmx
        print(f"Executing: {cmd}")
        subprocess.run(cmd, shell=True)

    def capture_memory_dump(self, snapshot_name, destination_path):
        """
        This function takes a snapshot of the running VM and copies the memory dump (.vmem) file
        to the specified destination directory.
        """
        if self.base_vmem_file is None:
            for file in os.listdir(self.vm_dir):
                if file.endswith('.vmem'):
                    self.base_vmem_file = file

        # Take the snapshot
        snapshot_cmd = self.vmrun + self.operation_map['createSnap'] + self.vmx + f' "{snapshot_name}"'
        print(f"Taking snapshot: {snapshot_cmd}")
        subprocess.run(snapshot_cmd, shell=True)

        # Assuming the .vmem file is in the same directory as the VMX file
        vm_dir = os.path.dirname(self.vm_dir.replace('"', ''))  # Remove quotes to get the actual path

        # Find the .vmem file (assuming it's the most recent .vmem file)
        vmem_file = None
        for file in os.listdir(vm_dir):
            if file.endswith('.vmem') and file != self.base_vmem_file:
                vmem_file = os.path.join(vm_dir, file)
                break

        # If we couldn't find the .vmem file, print an error and exit
        if not vmem_file or not os.path.exists(vmem_file):
            print(f"Error: Memory dump file for snapshot {snapshot_name} not found!")
            sys.exit(1)

        # Copy the memory dump to the destination
        dest_file = os.path.join(destination_path, f'{snapshot_name}.vmem')
        print(f"Copying memory dump from {vmem_file} to {dest_file}")
        shutil.copy(vmem_file, dest_file)
        print("Memory dump copied successfully.")

    def capture_initial_snapshot(self, snapshot_name, destination_path):
        """
        This function takes a snapshot of the running VM and copies the memory dump (.vmem) file
        to the specified destination directory.
        """
        if self.base_vmem_file is None:
            for file in os.listdir(self.vm_dir):
                if file.endswith('.vmem'):
                    self.base_vmem_file = file

        # Take the snapshot
        snapshot_cmd = self.vmrun + self.operation_map['createSnap'] + self.vmx + f' "{snapshot_name}"'
        print(f"Taking snapshot: {snapshot_cmd}")
        subprocess.run(snapshot_cmd, shell=True)

        # Assuming the .vmem file is in the same directory as the VMX file
        vm_dir = os.path.dirname(self.vm_dir.replace('"', ''))  # Remove quotes to get the actual path

        # Find the .vmem file (assuming it's the most recent .vmem file)
        vmem_file = None
        for file in os.listdir(vm_dir):
            if file.endswith('.vmem') and file != self.base_vmem_file:
                vmem_file = os.path.join(vm_dir, file)
                break

        # If we couldn't find the .vmem file, print an error and exit
        if not vmem_file or not os.path.exists(vmem_file):
            print(f"Error: Memory dump file for snapshot {snapshot_name} not found!")
            sys.exit(1)

        # Copy the memory dump to the destination
        dest_file = os.path.join(destination_path, f'{snapshot_name}.vmem')
        print(f"Copying memory dump from {vmem_file} to {dest_file}")
        shutil.copy(vmem_file, dest_file)
        self.initial_snapshot_name = snapshot_name
        print("Memory dump copied successfully.")

    def revert_to_initial_state(self):
        """
        Reverts the virtual machine to the initial snapshot.
        """
        # Revert to the initial snapshot
        revert_cmd = self.vmrun + self.operation_map['revertSnap'] + self.vmx + f' "{self.initial_snapshot_name}"'
        print(f"Reverting VM to initial snapshot: {revert_cmd}")
        subprocess.run(revert_cmd, shell=True)

    def revert_to_snapshot(self, snapshot_name: str):
        revert_cmd = self.vmrun + self.operation_map['revertSnap'] + self.vmx + f' "{snapshot_name}"'
        print(f"Reverting VM to initial snapshot: {revert_cmd}")
        subprocess.run(revert_cmd, shell=True)

    def run_program_in_guest(self, program, mode):
        """
        Run a program inside the guest VM.

        :param program: Path to the program inside the guest VM (e.g., "C:\\path\\to\\program.exe")
        :param mode: 'interactive' or 'background' (default is 'background')
        """
        if mode == 'interactive':
            cmd = f'{self.vmrun} -T ws runProgramInGuest {self.vmx} -activeWindow -interactive "{program}"'
        else:
            cmd = f'{self.vmrun} -T ws runProgramInGuest {self.vmx} "{program}"'

        print(f"Running program in guest: {cmd}")
        subprocess.run(cmd, shell=True)

    def operate_vm(self, operation: str):
        cmd = self.vmrun + self.operation_map[operation] + self.vmx
        print(f"Executing: {cmd}")
        subprocess.run(cmd, shell=True)

    @staticmethod
    def trim_paths(path: str):
        if ' ' in path and not path.startswith('"'):
            return f'"{path}"'

        return path