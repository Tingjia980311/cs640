# Sender (port 5000) ---- Emulator1 (port 3000) ---- Requester (port 4000)
# Sender (port 5100)

# run sender
python3 sender.py -p 5000 -g 4000 -r 100 -q 1 -l 10 -f rockhopper-03 -e 3000 -i 3 -t 1000

python3 sender.py -p 5100 -g 4000 -r 100 -q 1 -l 10 -f rockhopper-03 -e 3000 -i 3 -t 1000

# run emulator1 change the -q arg
python3 emulator.py -p 3000 -q 8 -f test/table -l log05

# run requester
python3 requester.py -p 4000 -f rockhopper-03 -e 3000 -o file_split.txt -w 10

