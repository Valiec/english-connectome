# Finds the median and MAD for all Mantel data, broken up by sample

# Usage: ./mantel_median_mad.sh <mantel data CSV>

echo "sample,signif,r" > data/mantel_median_mad.csv
python3 split_mantel.py $1;
for f in `ls data/mantel_data_*.csv`; do
	echo "Processing $f";
	rscript mantel_median_mad.R $f 2>/dev/null | sed "s/ ,/,/g" >> data/mantel_median_mad.csv;
done