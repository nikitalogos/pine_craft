rm -r out
rm -r out2
rm -r out3


echo "~~~~~~~~~~~~~~~~~~~~GEN-BOX~~~~~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~Let's double the box dimensions:~~~~~~~~~~"
pine-craft gen-box -o out --unit-size 60 --material-thickness 12 --hole-diameter 8


echo "~~~~~~~~~~~~~~~~~~~~GEN-PART~~~~~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~Let's scale part up by 1.25:~~~~~~~~~~"
pine-craft gen-part -o out/beam_5 -w 1 -t 5 --unit-size 37.5 --fillet-radius 6.25 --hole-diameter 5.01

echo "~~~~~~~~~~Make circular part with 6 holes:~~~~~~~~~~"
pine-craft gen-part -o out/circular_1 -w 1 -t 1 --fillet-radius 15 --holes-num 6

echo "~~~~~~~~~~Make part with big holes in the middle of units:~~~~~~~~~~"
pine-craft gen-part -o out/beam_10_big_holes -w 1 -t 10 --holes-num 1 --hole-diameter 10 --holes-ring-radius-norm 0

echo "~~~~~~~~~~Rotate holes at 45°:~~~~~~~~~~"
pine-craft gen-part -o out/beam_2_45_deg -w 1 -t 2 --first-hole-angle-deg 45

echo "~~~~~~~~~~Change pattern so that holes will go every second unit:~~~~~~~~~~"
pine-craft gen-part -o out/beam_5_sparse -w 1 -t 5 -p "x:1 y:2"



echo "~~~~~~~~~~Define pattern directly row by row. 'o' means holes, '.' means no holes:~~~~~~~~~~"
pine-craft gen-part -o out/plate_3x4_direct_pattern -w 3 -t 4 -p "ooo o.. oo. o.o"



echo "~~~~~~~~~~To make two patterns at the same time, pass pattern-specific parameters twice:~~~~~~~~~~"
pine-craft gen-part -o out/plate_5x5_2_patterns -w 5 -t 5 -p "x:4 y:4" -p "..... ..... ..o.. ..... ....."

echo "~~~~~~~~~~Let's make one regular pattern and one for big central holes in every second unit:~~~~~~~~~~"
pine-craft gen-part -o out/beam_5_2_patterns -w 1 -t 5 \
    --holes-num 4 --holes-ring-radius-norm 0.5 --hole-diameter 4 -p "x:1 y:1" \
    --holes-num 1 --holes-ring-radius-norm 0.0 --hole-diameter 6 -p "x:1 y:2"


echo "~~~~~~~~~~If you specify several patterns, pattern-specific parameters can be defined once if they don't change:~~~~~~~~~~"
pine-craft gen-part -o out/beam_15_2_patterns -w 1 -t 15 --holes-num 2 \
    --first-hole-angle-deg 90 -p "x:1 y:2" \
    --first-hole-angle-deg 0 -p "x:1 y:3"

echo "~~~~~~~~~~If some of patter-specific parameters is passed less times than the number of patterns, last patterns will use the last value of this parameter:~~~~~~~~~~"
pine-craft gen-part -o out/beam_4_4_patterns -w 1 -t 4 \
    -p "o..." --holes-num 1 --hole-diameter 2 \
    -p ".o.." --holes-num 2 --hole-diameter 4 \
    -p "..o." --holes-num 3 \
    -p "...o" \


echo "~~~~~~~~~~~~~~~~~~~~PLACE-PARTS~~~~~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~Place parts in a regular way~~~~~~~~~~"
pine-craft gen-part -o out/beam_3 -w 1 -t 3
pine-craft place-parts -i placing.yaml -o out
pine-craft cut-length -i out/placing/placing.dxf

echo "~~~~~~~~~~Place parts without deduplication: cut length is much bigger!~~~~~~~~~~"
pine-craft place-parts -i placing.yaml -o out2 --no-deduplicate
pine-craft cut-length -i out2/placing/placing.dxf

echo "~~~~~~~~~~Place parts with smaller hv_ratio: layout will change~~~~~~~~~~"
pine-craft place-parts -i placing.yaml -o out3 --hv-ratio 5
