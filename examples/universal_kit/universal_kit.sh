mkdir out
cd out || exit

# ~~~~~~~~~~~~~~~~generate parts~~~~~~~~~~~~~~~~~~~~~~
mkdir parts
cd parts || exit

# all beams
pine-craft gen-part -o beam_1 -w 1 -t 1
pine-craft gen-part -o beam_2 -w 1 -t 2
pine-craft gen-part -o beam_3 -w 1 -t 3
pine-craft gen-part -o beam_5 -w 1 -t 5
pine-craft gen-part -o beam_7 -w 1 -t 7
pine-craft gen-part -o beam_10 -w 1 -t 10
pine-craft gen-part -o beam_14 -w 1 -t 14
pine-craft gen-part -o beam_20 -w 1 -t 20

# dense plates
pine-craft gen-part -o plate_2x2 -w 2 -t 2
pine-craft gen-part -o plate_5x10 -w 5 -t 10
pine-craft gen-part -o plate_10x10 -w 10 -t 10
pine-craft gen-part -o plate_10x15 -w 10 -t 15
pine-craft gen-part -o plate_10x20 -w 10 -t 20

# sparse plates
pine-craft gen-part -o plate_10x10_sparse -w 10 -t 10 -p "x:4,1 y:4,1"
pine-craft gen-part -o plate_10x15_sparse -w 10 -t 15 -p "x:4,1 y:4,1"
pine-craft gen-part -o plate_10x20_sparse -w 10 -t 20 -p "x:4,1 y:4,1"
pine-craft gen-part -o plate_10x30_sparse -w 10 -t 30 -p "x:4,1 y:4,1"

# experimental plates
pine-craft gen-part -o plate_2x3 -w 2 -t 3
pine-craft gen-part -o plate_2x4 -w 2 -t 4
pine-craft gen-part -o plate_3x3 -w 3 -t 3

# box parts
pine-craft gen-box

# ~~~~~~~~~~~~~~~~place parts~~~~~~~~~~~~~~~~~~~~~~
cd ../..

pine-craft place-parts -i placing_beams_and_plates.yaml -o out --hv_ratio 100000
pine-craft place-parts -i placing_boxes.yaml -o out --hv_ratio 100000