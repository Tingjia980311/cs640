Sender(port 5000) ---- Emulator(port 3000) -----Requester (port 4000)

# run sender
python3 sender.py -p 5000 -g 4000 -r 100 -q 1 -l 10 -f rockhopper-03 -e 3000 -i 3 -t 1000

# run emulator
python3 emulator.py -p 3000 -q 100 -f test/table1 -l log01

# run requester
python3 requester.py -p 4000 -f rockhopper-03 -e 3000 -o file.txt -w 10

