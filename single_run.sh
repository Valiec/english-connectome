touch logs/"$1".in_progress; # save temp file
# shellcheck disable=SC2086
python3 -u bfs_parallel.py samples/etym_sample_"$1".csv samples/node_sample_"$1".txt "$1" > logs/log_bfs_etym_"$1".txt; # run etym distances
python3 -u bfs_parallel.py samples/sem_sample_"$1".csv samples/node_sample_"$1".txt "$1" > logs/log_bfs_sem_"$1".txt; # run sem distances
rm logs/"$1".in_progress; # remove temp file
