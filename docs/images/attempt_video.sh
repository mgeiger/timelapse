APP=/usr/bin/avconv
DATE=$(date --iso-8601)

# Don't know what I was going for here
OPT="-an"

# This generates some files that avconv can actually read
x=0
for i in `ls *.jpg`; do
    counter=$(printf %05d $x);
    ln -s "$i" "$counter".jpg;
    x=$(($x+1));
done

# Makes a new video using the links setup previously
RATE="-r 24"
IN="-i %05d.jpg"
CODEC="-codec:v libx264"
FRAME="-bf 2"
FLAG="-flags +cgop"
QUALITY="-crf 21"
$APP $RATE $IN $RATE $CODEC $FRAME $FLAG $QUALITY -g 12 $DATE.mp4

# Now we need to remove everything that we don't want.
# How about we keep one image every hour?
