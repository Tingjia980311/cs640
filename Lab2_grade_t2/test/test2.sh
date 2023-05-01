# Sender (port 5000) ---- Emulator1 (port 6000) ---- Emulator2 (port 3000) ---- Requester (port 4000)

# run sender
python3 sender.py -p 5000 -g 4000 -r 100 -q 1 -l 10 -f rockhopper-03 -e 6000 -i 3 -t 1000

# run emulator1
python3 emulator.py -p 6000 -q 100 -f test/table2 -l log02

# run emulator2
python3 emulator.py -p 3000 -q 100 -f test/table2 -l log12

# run requester
python3 requester.py -p 4000 -f rockhopper-03 -e 3000 -o file.txt -w 10

