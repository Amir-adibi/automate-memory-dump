import sys
import os
import subprocess
import shutil

# Automate Operations on a single VM
class VM:
    operation_map = {
        'start': r' -T ws start ',
        'stop': r' -T ws stop ',

        'createSnap': r' -T ws snapshot ',
        'revertSnap': r' -T ws revertToSnapshot ',
    }

    def __init__(self, vmrun_path: str, vmx_path: str, initial_snapshot_name: str):
        self.vmrun = vmrun_path
        self.vmx = vmx_path
        self.initial_snapshot_name = initial_snapshot_name

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
        # Take the snapshot
        snapshot_cmd = self.vmrun + self.operation_map['createSnap'] + self.vmx + f' "{snapshot_name}"'
        print(f"Taking snapshot: {snapshot_cmd}")
        subprocess.run(snapshot_cmd, shell=True)

        # Assuming the .vmem file is in the same directory as the VMX file
        vm_dir = os.path.dirname(self.vmx.replace('"', ''))  # Remove quotes to get the actual path
        memory_file = os.path.join(vm_dir,
                                   f'{os.path.splitext(os.path.basename(self.vmx))[0]}-Snapshot{snapshot_name}.vmem')

        # Ensure the memory dump exists
        if not os.path.exists(memory_file):
            print(f"Error: Memory dump file {memory_file} not found!")
            sys.exit(1)

        # Copy the memory dump to the destination
        dest_file = os.path.join(destination_path, f'{snapshot_name}.vmem')
        print(f"Copying memory dump from {memory_file} to {dest_file}")
        shutil.copy(memory_file, dest_file)
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


    def operate_vm(self, operation: str):
        cmd = self.vmrun + self.operation_map[operation] + self.vmx
        print(f"Executing: {cmd}")
        subprocess.run(cmd, shell=True)