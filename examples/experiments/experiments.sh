rm -r out
rm -r out2
rm -r out3


echo '~~~~~~~~~~~~~~~~~~~~GEN-BOX~~~~~~~~~~~~~~~~~~~~'
echo "~~~~~~~~~~Let's double the box dimensions:~~~~~~~~~~"
pine-craft gen-box -o out --unit-size 60 --material-thickness 12 --hole-diameter 8


echo '~~~~~~~~~~~~~~~~~~~~GEN-PART~~~~~~~~~~~~~~~~~~~~'
echo "~~~~~~~~~~Let's scale part up by 1.25:~~~~~~~~~~"
pine-craft gen-part -o out/beam_5 -w 1 -t 5 --unit-size 37.5 --fillet-radius 6.25 --hole-diameter 5.01

echo '~~~~~~~~~~~~~~~~~~~~PLACE-PARTS~~~~~~~~~~~~~~~~~~~~'
echo '~~~~~~~~~~Place parts in a regular way~~~~~~~~~~'
pine-craft gen-part -o out/beam_3 -w 1 -t 3
pine-craft place-parts -i placing.yaml -o out
pine-craft cut-length -i out/placing/placing.dxf

echo '~~~~~~~~~~Place parts without deduplication: cut length is much bigger!~~~~~~~~~~'
pine-craft place-parts -i placing.yaml -o out2 --no-deduplicate
pine-craft cut-length -i out2/placing/placing.dxf

echo '~~~~~~~~~~Place parts with smaller hv_ratio: layout will change~~~~~~~~~~'
pine-craft place-parts -i placing.yaml -o out3 --hv-ratio 5 -v
