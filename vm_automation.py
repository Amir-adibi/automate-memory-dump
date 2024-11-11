import glob
import os
import shutil
import time
from vmrun import Vmrun

class VMAutomation:
    def __init__(self, vmx, vmrun_path, user, password, clean_snapshot_name, malware_dir_guest, snapshot_dir_host, vm_path):
        self.vm = Vmrun(vmx=vmx, user=user, password=password, vmrun=vmrun_path, product='ws', debug=False)
        self.clean_snapshot_name = clean_snapshot_name
        self.malware_dir_guest = malware_dir_guest  # Directory where malware is stored in the guest OS
        self.snapshot_dir_host = snapshot_dir_host  # Directory on the host for storing memory dumps
        self.vm_path = vm_path

    def run(self, app_path):
        return self.vm.runProgramInGuest(app_path, mode="i")

    def run_malware(self, malware_name):
        # Run the malware executable inside the guest OS
        malware_path = f'"{self.malware_dir_guest}\\{malware_name}"'
        print(f"Running malware in guest: {malware_path}")
        return self.vm.runProgramInGuest(malware_path, mode="i")  # 'i' = interactive

    def capture_snapshot(self, malware_name):
        # Take a snapshot with the malware name and move its associated memory dump
        snapshot_name = f"{malware_name}"
        print(f"Taking snapshot: {snapshot_name}")
        self.vm.snapshot(snapshot_name)

    def revert_to_clean_state(self):
        # Revert the virtual machine back to the clean snapshot state
        print(f"Reverting to clean state: {self.clean_snapshot_name}")
        self.vm.revertToSnapshot(self.clean_snapshot_name)

    def start(self):
        self.vm.start()

    def delete_file_in_guest(self, malware_name):
        try:
            malware_path = f'"{self.malware_dir_guest}\\{malware_name}"'
            self.vm.deleteFileInGuest(malware_path)
        except Exception as e:
            print(f"Error deleting malware: {e}")

    def delete_malware(self, malware_name):
        self.revert_to_clean_state()
        self.start()
        time.sleep(7)
        self.delete_file_in_guest(malware_name)
        self.delete_snapshot("clean_state")
        self.capture_snapshot("clean_state")

    def delete_snapshot(self, snapshot_name):
        try:
            self.vm.deleteSnapshot(snapshot_name)
        except Exception as e:
            print(f"Error deleting snapshot: {e}")

    def automate(self):
        # Get a list of malware files inside the guest OS directory
        malware_files = self.vm.listDirectoryInGuest(self.malware_dir_guest)
        malware_files = [f for f in malware_files if ".exe" in f]

        for malware in malware_files:
            malware = malware.strip()
            malware_name = malware.split("\\")[-1]  # Get the malware filename

            # Run the malware
            cmd_result = self.run_malware(malware_name)
            cmd_output = ''.join([line for line in cmd_result])
            print("CMD_RESULT: ", cmd_output)
            if 'could not run on the guest' in cmd_output:
                self.delete_malware(malware_name)
                continue

            # Wait for 120 seconds for the malware to execute
            print(f"Waiting 120 seconds for malware: {malware_name}")
            time.sleep(120)

            # Capture the snapshot after running the malware
            self.capture_snapshot(malware_name)

            vmem_path = self.get_newest_vmem_file(self.vm_path)
            self.move_and_rename_vmem_file(vmem_path, self.snapshot_dir_host, malware_name + '.vmem')

            # Revert back to the clean snapshot state
            self.revert_to_clean_state()
            self.start()
            time.sleep(7)

            print(f"Malware {malware_name} execution completed.\n")

    @staticmethod
    def get_newest_vmem_file(directory):
        vmem_files = glob.glob(os.path.join(directory, "*.vmem"))

        if not vmem_files:
            print("No vmem files found!")
            return None

        newest_file = max(vmem_files, key=os.path.getctime)

        return newest_file

    @staticmethod
    def move_and_rename_vmem_file(src_path: str, dest_dir: str, new_name: str):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        dst_path = os.path.join(dest_dir, new_name)

        try:
            shutil.move(src_path, dst_path)
            print(f"**** Moved {src_path} to {dst_path}")
        except Exception as e:
            print(f"**** Error moving the file: {e}")