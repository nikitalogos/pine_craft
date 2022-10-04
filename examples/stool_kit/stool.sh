mkdir out
cd out || exit

# ~~~~~~~~~~~~~~~~generate parts~~~~~~~~~~~~~~~~~~~~~~
mkdir parts
cd parts || exit

# all beams
pine-craft gen-part -o beam_3 -w 1 -t 3
pine-craft gen-part -o beam_5 -w 1 -t 5
pine-craft gen-part -o beam_10 -w 1 -t 10
pine-craft gen-part -o beam_14 -w 1 -t 14

# sparse plates
pine-craft gen-part -o plate_10x10_sparse -w 10 -t 10 -p "x:4,1 y:4,1"

# box parts
pine-craft gen-box

# ~~~~~~~~~~~~~~~~place parts~~~~~~~~~~~~~~~~~~~~~~
cd ../..

pine-craft place-parts -i stool.yaml -o out --hv_ratio 100000