rm -r out

echo '~~~~~~~~~~Creating regular parts~~~~~~~~~~'
pine-craft gen-part -o out/beam_3 -w 1 -t 3
pine-craft gen-part -o out/beam_5_sparse -w 1 -t 5 -p "x:1 y:2"
pine-craft gen-part -o out/plate_10x10_sparse -w 10 -t 10 -p "x:4,1 y:4,1"

echo '~~~~~~~~~~Creating box parts~~~~~~~~~~'
pine-craft gen-box -o out

echo '~~~~~~~~~~Place parts on sheet for CNC cutting~~~~~~~~~~'
pine-craft place-parts -i placing.yaml -o out

echo '~~~~~~~~~~Compute total cutting length~~~~~~~~~~'
pine-craft cut-length -i out/placing/placing.dxf