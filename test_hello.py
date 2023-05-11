import socket
import os
from random import choice
from string import ascii_uppercase
import argparse
import subprocess
import shutil
import time
import io
import signal
import pexpect
import threading
import psutil

def test():
    # Let the emulator handle SIGINT signal so that we can use os.kill to kill it in the script
    os.system("cp ../josephkevin/*.py ./")
    sed_cmd = "sed -i \"1i signal.signal(signal.SIGINT, signal_handler)\" ./emulator.py"
    os.system(sed_cmd)
    sed_cmd = "sed -i \"1i\ \texit()\" ./emulator.py"
    os.system(sed_cmd)
    sed_cmd = "sed -i \"1i def signal_handler(sig, frame):\" ./emulator.py"
    os.system(sed_cmd)
    sed_cmd = "sed -i \"1i import signal\" ./emulator.py"
    os.system(sed_cmd)

    # Folder paths
    emulator_dirs = [
        "emulator1",
        "emulator2",
    ]

    # Ports
    emulator_ports = [
        "6001",
        "6002",
    ]

    # Emulator ip + ports
    ip = socket.gethostbyname(socket.gethostname())
    emu1 = ip + ',6001'
    emu2 = ip + ',6002'

    # Topology file text
    topo = emu1 + ' ' + emu2 + '\n'
    topo += emu2 + ' ' + emu1  + '\n'

    procs = []

    for i in range(len(emulator_dirs)):
        emu_path = os.path.join("./", emulator_dirs[i])
        emu_python_path = os.path.join(emu_path, "emulator.py")
        emu_topo_path = os.path.join(emu_path, "topology.txt")

        try:
            os.mkdir(emu_path)
        except FileExistsError:
            pass

        # copy the python files to each emulator dir
        os.system("cp *.py " + emu_path)
        # generate the topology file
        f = open(emu_topo_path, 'w')
        f.write(topo)
        f.close()

        # start the emulator and redirect the result to output.txt
        os.chdir(emu_path)
        cmd_str = ' '.join(["python3", "./emulator.py", "-p", emulator_ports[i], "-f", "./topology.txt", "> output.txt", "&"])
        with open("output.txt","w") as f:
            procs.append(subprocess.Popen(cmd_str, shell = True))
        os.chdir('../')

    # sleep 5 seconds to make the network stable
    time.sleep(5)
    # kill node 2
    kill_snd_emulator = 0
    while not kill_snd_emulator:
        kill_snd_emulator = 1
        for process in psutil.process_iter(['name']):
            if process.info['name'] == 'python3':
                if len(process.cmdline()) < 2:
                    continue
                if process.cmdline()[1] == './emulator.py':
                    if process.cmdline()[3] == '6002':
                        os.system("kill -2 " + str(process.pid))
                        kill_snd_emulator = 0

    # wait for 5 seconds
    time.sleep(5)

    # restart node 2
    os.chdir(emulator_dirs[1])
    cmd_str = ' '.join(["python3", "./emulator.py", "-p", emulator_ports[1], "-f", "./topology.txt", "> output.txt", "&"])
    with open("output.txt","w") as f:
        procs.append(subprocess.Popen(cmd_str, shell = True))
    os.chdir('../')

    # wait for 5 seconds
    time.sleep(5)

    # kill all emulators with SIGINT, and the stdout from emulator will flush to output.txt
    kill_finish = 0
    while not kill_finish:
        kill_finish = 1
        for process in psutil.process_iter(['name']):
            if process.info['name'] == 'python3':
                if len(process.cmdline()) < 2:
                    continue
                if process.cmdline()[1] == './emulator.py':
                    print("kill ", process.pid)
                    # os.kill(process.pid, signal.SIGINT)
                    os.system("kill -2 " + str(process.pid))
                    kill_finish = 0

    # print the output of node 1
    for i in range(len(emulator_dirs)):
        print("--------------------------------------output for emulator " + str(i) + " --------------------------------------")
        emu_path = os.path.join("./", emulator_dirs[i])
        os.chdir(emu_path)
        os.system("cat output.txt")
        os.chdir('../')
        break

    # cleanup
    for i in range(len(emulator_dirs)):
        emu_path = os.path.join("./", emulator_dirs[i])
        os.system("rm -rf " + emu_path)
test()   
