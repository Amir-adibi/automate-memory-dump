# vm = Vmrun(
#     vmx=r"C:\Users\Amir\Documents\Virtual Machines\Windows 10 x64\Windows 10 x64.vmx",
#     user="Amir",
#     password="a123",
#     vmrun=r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe",
#     debug=False,
#     product='ws'
# )
#
# snapshots_list = vm.listSnapshots()
# print(snapshots_list[1])
# result = os.listdir(r'"C:\Users\Amir\Documents\Virtual Machines\Windows 10 x64"')
# print(result)


# vm.start()
# vm.runProgramInGuest(r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"', "i")
#
# malware_directory = r'"C:\Users\Amir\Desktop\Dataset\Malware"'
# number_of_malware = 997
#
# for i in range(1, 998):
#     vm.runProgramInGuest()
#     pass

# C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe -T ws -gu Amir -gp a123 runProgramInGuest "C:\Users\Amir\Documents\Virtual Machines\Windows 10 x64\Windows 10 x64.vmx" -interactive "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
