import os

from malware_automation import MalwareAutomation
from vmrun import Vmrun

vm = Vmrun(
    vmx=r"C:\Users\Amir\Documents\Virtual Machines\Windows 10 x64\Windows 10 x64.vmx",
    user="Amir",
    password="a123",
    vmrun=r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe",
    debug=False,
    product='ws'
)

snapshots_list = vm.listSnapshots()
print(snapshots_list[1])
result = os.listdir(r'"C:\Users\Amir\Documents\Virtual Machines\Windows 10 x64"')
print(result)


# vm.start()
# vm.runProgramInGuest(r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"', "i")
#
# malware_directory = r'"C:\Users\Amir\Desktop\Dataset\Malware"'
# number_of_malware = 997
#
# for i in range(1, 998):
#     vm.runProgramInGuest()
#     pass

# automation = MalwareAutomation(
#     vmx=r"C:\Users\Amir\Documents\Virtual Machines\Windows 10 x64\Windows 10 x64.vmx",
#     vmrun_path=r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe",
#     user="Amir",
#     password="a123",
#     clean_snapshot_name=r"Windows 10 x64-Snapshot20",
#     malware_dir_guest= r"C:\Users\Amir\Desktop\Dataset\Malware",
#     snapshot_dir_host= r"C:\Users\Amir\Desktop\Git\project\vmrun-python\snapshots",
# )
#
# automation.automate()

# C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe -T ws -gu Amir -gp a123 runProgramInGuest "C:\Users\Amir\Documents\Virtual Machines\Windows 10 x64\Windows 10 x64.vmx" -interactive "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
