# Runs the Mantel test on all samples

# Usage: ./mantel.sh

echo "sample,signif,r" > data/mantel_data.csv
for i in `seq 1 720`; do
	echo "Processing $i";
	python3 to_matrix.py distances/sem_sample_$i.$i.deep_pdistances.csv distances/etym_sample_$i.$i.deep_pdistances.csv;
	printf "sample_%s," $i >> data/mantel_data.csv;
	rscript mantel.R matrices/sem_sample_$i.$i.deep_pdistances_mat.csv matrices/etym_sample_$i.$i.deep_pdistances_mat.csv 2>/dev/null | sed "s/ ,/,/g" >> data/mantel_data.csv;
done

python3 aggregate_mantel.py data/mantel_data.csv > data/mantel_summary.csv;