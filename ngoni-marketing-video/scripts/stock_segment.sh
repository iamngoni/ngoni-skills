#!/bin/zsh
# Cut one graded segment from a licensed stock clip without downloading it whole.
# Usage: stock_segment.sh <source.mp4|url> <out.mp4> <start_s> <dur_s> <src_w> <src_h> [aspect 1:1|9:16|16:9|4:5] [centre_x 0..1] [brightness]
# Default grade: slightly warm, -10% saturation, lifted blacks. Tune G to the project's look. Output 30 fps H.264.
set -e
src=$1; out=$2; ss=$3; d=$4; W=$5; H=$6; asp=${7:-1:1}; cx=${8:-0.5}; br=${9:-0}
G="colorbalance=rs=0.05:bs=-0.05:rm=0.03:bm=-0.04:rh=0.02:bh=-0.03,eq=contrast=1.04:saturation=0.9:brightness=${br},curves=all='0/0.035 1/0.98'"
read aw ah ow oh <<< $(python3 -c "
a={'1:1':(1,1,1080,1080),'9:16':(9,16,1080,1920),'16:9':(16,9,1920,1080),'4:5':(4,5,1080,1350)}['$asp']
print(*a)")
read cw ch x y <<< $(python3 -c "
W,H,aw,ah,cx=$W,$H,$aw,$ah,$cx
cw,ch=(W,int(W*ah/aw)) if W*ah/aw<=H else (int(H*aw/ah),H)
x=max(0,min(W-cw,int(W*cx-cw/2))); y=(H-ch)//2
print(cw,ch,x,y)")
ffmpeg -hide_banner -loglevel error -y -ss $ss -t $d -i "$src" -an \
  -vf "crop=${cw}:${ch}:${x}:${y},scale=${ow}:${oh}:flags=lanczos,fps=30,$G,format=yuv420p" \
  -c:v libx264 -crf 20 -preset medium -movflags +faststart "$out"
echo "done $out ($asp)"
