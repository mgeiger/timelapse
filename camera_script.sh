while true
do
	NAME=$(date --iso-8601=seconds)
	echo "Saving $NAME"
	raspistill --verbose --output $NAME.jpg
	sleep 15
done
