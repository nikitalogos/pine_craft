mkdir out
cd out || exit

# ~~~~~~~~~~~~~~~~generate parts~~~~~~~~~~~~~~~~~~~~~~
mkdir parts
cd parts || exit

# all beams
../../../entry_points/gen_part.py -n beam_1 -w 1 -t 1
../../../entry_points/gen_part.py -n beam_2 -w 1 -t 2
../../../entry_points/gen_part.py -n beam_3 -w 1 -t 3
../../../entry_points/gen_part.py -n beam_5 -w 1 -t 5
../../../entry_points/gen_part.py -n beam_7 -w 1 -t 7
../../../entry_points/gen_part.py -n beam_10 -w 1 -t 10
../../../entry_points/gen_part.py -n beam_14 -w 1 -t 14
../../../entry_points/gen_part.py -n beam_20 -w 1 -t 20

# dense plates
../../../entry_points/gen_part.py -n plate_2x2 -w 2 -t 2
../../../entry_points/gen_part.py -n plate_5x10 -w 5 -t 10
../../../entry_points/gen_part.py -n plate_10x10 -w 10 -t 10
../../../entry_points/gen_part.py -n plate_10x15 -w 10 -t 15
../../../entry_points/gen_part.py -n plate_10x20 -w 10 -t 20

# sparse plates
../../../entry_points/gen_part.py -n plate_10x10_sparse -w 10 -t 10 -p "x:4,1 y:4,1"
../../../entry_points/gen_part.py -n plate_10x15_sparse -w 10 -t 15 -p "x:4,1 y:4,1"
../../../entry_points/gen_part.py -n plate_10x20_sparse -w 10 -t 20 -p "x:4,1 y:4,1"
../../../entry_points/gen_part.py -n plate_10x30_sparse -w 10 -t 30 -p "x:4,1 y:4,1"

# experimental plates
../../../entry_points/gen_part.py -n plate_2x3 -w 2 -t 3
../../../entry_points/gen_part.py -n plate_2x4 -w 2 -t 4
../../../entry_points/gen_part.py -n plate_3x3 -w 3 -t 3

# box parts
../../../entry_points/make_box_parts.py

# ~~~~~~~~~~~~~~~~place parts~~~~~~~~~~~~~~~~~~~~~~
cd ..

../../entry_points/place_parts.py -c ../placing_1_config.yaml -n placing_1 --hv_ratio 100000
../../entry_points/place_parts.py -c ../placing_2_config.yaml -n placing_2 --hv_ratio 100000