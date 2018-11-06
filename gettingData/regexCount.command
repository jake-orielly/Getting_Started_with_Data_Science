cd `dirname $0`
cat someFile.txt | python egrep.py "[0-9]" | python line_count.py