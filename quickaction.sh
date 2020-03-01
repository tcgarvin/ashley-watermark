for f in "$@"
do
	osascript -e "tell app \"Terminal\" to do script \"~/watermark.sh '$f'\"" -e 'tell app "Terminal" to activate'
done