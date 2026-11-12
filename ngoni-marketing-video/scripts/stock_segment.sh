#!/bin/zsh
# Cut one graded square segment from a licensed stock clip without downloading it whole.
# Usage: stock_segment.sh <source.mp4|url> <out.mp4> <start_s> <dur_s> <src_w> <src_h> [centre_x 0..1] [brightness]
# Grade matches the house look: slightly warm, -10% saturation, lifted blacks. Output 1080x1080, 30 fps, H.264.
set -e
src=$1; out=$2; ss=$3; d=$4; W=$5; H=$6; cx=${7:-0.5}; br=${8:-0}
G="colorbalance=rs=0.05:bs=-0.05:rm=0.03:bm=-0.04:rh=0.02:bh=-0.03,eq=contrast=1.04:saturation=0.9:brightness=${br},curves=all='0/0.035 1/0.98'"
cw=$(( W < H ? W : H ))
x=$(python3 -c "print(max(0,min($W-$cw,int($W*$cx-$cw/2))))")
ffmpeg -hide_banner -loglevel error -y -ss $ss -t $d -i "$src" -an \
  -vf "crop=$cw:$cw:$x:$(( (H-cw)/2 )),scale=1080:1080:flags=lanczos,fps=30,$G,format=yuv420p" \
  -c:v libx264 -crf 20 -preset medium -movflags +faststart "$out"
echo "done $out"
