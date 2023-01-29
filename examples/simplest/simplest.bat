call ..\..\venv\Scripts\activate.bat

rd /s /q out

echo '~~~~~~~~Creating regular parts~~~~~~'
py ..\..\pine-craft.py gen-part -o out/beam_3 -w 1 -t 3
py ..\..\pine-craft.py gen-part -o out/beam_5_sparse -w 1 -t 5 -p "x:1 y:2"
py ..\..\pine-craft.py gen-part -o out/plate_10x10_sparse -w 10 -t 10 -p "x:4,1 y:4,1"

echo '~~~~~~Creating box parts~~~~~~'
py ..\..\pine-craft.py gen-box -o out

echo '~~~~~~Place parts on sheet for CNC cutting~~~~~~'
py ..\..\pine-craft.py place-parts -i placing.yaml -o out

echo '~~~~~~Compute total cutting length~~~~~~~~'
py ..\..\pine-craft.py cut-length -i out/placing/placing.dxf