# Runs a batch of 20 analyses

# Usage ./analyse_set.sh <starting sample number> <ending sample number>

for i in `seq $1 $2`; do # run all samples between $1 and $2
	echo "Starting run $i"; # log
	./single_run.sh $i & # run sample and detatch so more can be started in parallel
done; 
wait # wait for all runs to finish

