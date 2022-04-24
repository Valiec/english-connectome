echo "sample,sem_avg,etym_avg" > data/$3.csv # write header (and blank file if it exists)
for i in `seq $1 $2`; do # for all samples
	echo "Processing $i" # log
	python3 average_file.py distances/sem_sample_$i.$i.deep_pdistances.csv distances/etym_sample_$i.$i.deep_pdistances.csv >> data/$3.csv; # average sample and append to file
done