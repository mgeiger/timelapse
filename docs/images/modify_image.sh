DATE=$(date --iso-8601=seconds)
OUTFILE=labeled/$DATE.jpg

echo $1

#convert $1 -gravity South -annotate 0 '%f' labeled/$1 
convert $1 -pointsize 20 -gravity SouthWest -stroke '#000C' -strokewidth 2 -annotate +10+10 '%f' -stroke none -fill white -annotate +10+10 '%f' $OUTFILE

convert $1 -pointsize 20 -gravity SouthWest -stroke '#000C' -strokewidth 2 -annotate +10+10 '%f' -stroke none -fill white -annotate +10+10 '%f' $OUTFILE

# check out AVConv later
# "avconv -r %s -i image%s.jpg -r %s -vcodec libx264 -crf 20 -g 15 -vf crop=2592:1458,scale=1280:720 timelapse.mp4"%(FPS_IN,'%7d',FPS_OUT))


#convert 2017-02-04T16\:43\:00-0500.jpg -gravity SouthWest -annotate 0 '%f' labeled/output.jpg
