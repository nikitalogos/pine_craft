mkdir default_parts
cd default_parts

# all beams
../genpart.py -n beam_1 -w 1 -t 1
../genpart.py -n beam_2 -w 1 -t 2
../genpart.py -n beam_3 -w 1 -t 3
../genpart.py -n beam_5 -w 1 -t 5
../genpart.py -n beam_7 -w 1 -t 7
../genpart.py -n beam_10 -w 1 -t 10
../genpart.py -n beam_14 -w 1 -t 14
../genpart.py -n beam_20 -w 1 -t 20

# dense plates
../genpart.py -n plate_2x2 -w 2 -t 2
../genpart.py -n plate_5x10 -w 5 -t 10
../genpart.py -n plate_10x10 -w 10 -t 10
../genpart.py -n plate_10x15 -w 10 -t 15
../genpart.py -n plate_10x20 -w 10 -t 20

# sparse plates
../genpart.py -n plate_10x10_sparse -w 10 -t 10 -p "x:4,1 y:4,1"
../genpart.py -n plate_10x15_sparse -w 10 -t 15 -p "x:4,1 y:4,1"
../genpart.py -n plate_10x20_sparse -w 10 -t 20 -p "x:4,1 y:4,1"

# experimental plates
../genpart.py -n plate_2x3 -w 2 -t 3
../genpart.py -n plate_2x4 -w 2 -t 4
../genpart.py -n plate_3x3 -w 3 -t 3
