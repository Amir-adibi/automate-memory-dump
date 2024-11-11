import os

from malware_automation import VMAutomation
from vmrun import Vmrun


automation = VMAutomation(
    vmx=r"C:\Users\Amir\Documents\Virtual Machines\Windows 10 x64\Windows 10 x64.vmx",
    vmrun_path=r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe",
    user="Amir",
    password="a123",
    clean_snapshot_name=r"clean_state",
    malware_dir_guest= r"C:\Users\Amir\Desktop\Dataset\Malware",
    snapshot_dir_host= r"C:\Users\Amir\Desktop\Git\project\vmrun-python\snapshots",
    vm_path=r"C:\Users\Amir\Documents\Virtual Machines\Windows 10 x64"
)

automation.automate()

