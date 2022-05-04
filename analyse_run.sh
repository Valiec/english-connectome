# Runs an analysis run in batches of 20

# Usage ./analyse_run.sh <node list> <edge list 1> <edge list 2> <sample count> <sample size> <starting sample number>

python3 sample_nodes.py $1 $2 $3 $4 $5 node_sample sem_sample etym_sample $6; # create node and edge samples
index=$(($6 + 1)); # init starting sample number
next=$(($6 + 20)); # init ending sample number for each batch of 20
for i in `seq 1 4`; do
	./analyse_set.sh $index $next 20 $5; # run batch of 20
	# update sample numbers for next batch
	index=$(($index + 20));
	next=$(($next + 20));
done
