# Get yesterday's date
YEAR=$(date -d "yesterday 13:00 " '+%Y')
MONTH=$(date -d "yesterday 13:00 " '+%m')
DAY=$(date -d "yesterday 13:00 " '+%d')
DATE=$(date -d "yesterday 13:00 " '+%Y-%m-%d')

# Locatoin of the files we will be working with
BASE=/opt/camera
DIR=$BASE/$YEAR/$MONTH/$DAY

APP=/usr/bin/mencoder

# Options for the mencoder
OPT="-nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1280:720"
IN="-mf type=jpeg:fps=24 mf://@$DIR/$DATE.txt"
OUT="-o $DIR/$DATE.avi"

# Get the files I want to encode
ls /$DIR/*.jpg > /$DIR/$DATE.txt

# Run the application
$APP $OPT $OUT $IN

