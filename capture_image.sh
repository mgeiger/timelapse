PROG=/usr/bin/raspistill
OPT="--height 720 --width 1280 --output"
BASE=/opt/camera
STORE=$BASE/$(date +%Y)/$(date +%m)/$(date +%d)
DATE=$(date --iso-8601=seconds)
FILE=$DATE.jpg

# Check to see if we have a place to store files
if [ ! -d "$STORE" ]; then
    echo "Making directory $STORE"
    mkdir -p $STORE
fi

# Run the Raspistill Command
echo "$PROG $OPT $STORE/$FILE"
$PROG $OPT $STORE/$FILE

# Add in a timestamp to the image
CONV=/usr/bin/convert
C_OPT1="-pointsize 20 -gravity SouthWest"
C_OPT2="-stroke '#000C' -strokewidth 2 -annotate +10+10 $DATE"
C_OPT3="-stroke none -fill white -annotate +10+10 $DATE"
$CONV $STORE/$FILE $C_OPT1 $C_OPT2 $C_OPT3 $STORE/$FILE
