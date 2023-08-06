# -*- coding: utf-8 -*-
'''
  ____  ___   ____________  ___  ___  ____     _________________
 / __ \/ _ | / __/  _/ __/ / _ \/ _ \/ __ \__ / / __/ ___/_  __/
/ /_/ / __ |_\ \_/ /_\ \  / ___/ , _/ /_/ / // / _// /__  / /   
\____/_/ |_/___/___/___/ /_/  /_/|_|\____/\___/___/\___/ /_/    
         Operational Aid Source for Infra-Structure 

Created on 2020. 3. 18..
@author: Hye-Churn Jang, CMBU Specialist in Korea, VMware [jangh@vmware.com]
'''

from vvv_vra import *

SDK.VRA.system('https://vra.vmkloud.com', 'jangh', 'David*#8090')

# vm = Machine('9fe0f5fcc4f8b427')
# print(vm)
# print(vm.Operations)
# print(vm.Disks)
# print(vm.Disk.list())

print(Machine.SnapShot.__help__())