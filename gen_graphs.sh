# Renders subsets of the connectome graphs.

# Usage: ./gen_graphs.sh <central word 1> <central word 2> <depth> <downsampling for word 1 sem> <downsampling for word 2 sem> <downsampling for word 1 etym> <downsampling for word 2 etym>

python3 select_node_set.py data/sem_links.csv $1 $3 $4 $8 > data/$1_sem_$3.csv
python3 select_node_set.py data/sem_links.csv $2 $3 $5 $8 > data/$2_sem_$3.csv
python3 select_node_set.py data/etym_links.csv $1 $3 $6 $8 > data/$1_etym_$3.csv
python3 select_node_set.py data/etym_links.csv $2 $3 $7 $8 > data/$2_etym_$3.csv

printf "$1_sem_$3 " > logs/nodelog_$1_$2_$3_$4_$5_$6_$7_$8.txt
python3 graph_network.py data/$1_sem_$3.csv | wc -l >> logs/nodelog_$1_$2_$3_$4_$5_$6_$7_$8.txt
printf "$2_sem_$3 " >> logs/nodelog_$1_$2_$3_$4_$5_$6_$7.txt
python3 graph_network.py data/$2_sem_$3.csv | wc -l >> logs/nodelog_$1_$2_$3_$4_$5_$6_$7_$8.txt
printf "$1_etym_$3 " >> logs/nodelog_$1_$2_$3_$4_$5_$6_$7.txt
python3 graph_network.py data/$1_etym_$3.csv | wc -l >> logs/nodelog_$1_$2_$3_$4_$5_$6_$7_$8.txt
printf "$2_etym_$3 " >> logs/nodelog_$1_$2_$3_$4_$5_$6_$7.txt
python3 graph_network.py data/$2_etym_$3.csv | wc -l >> logs/nodelog_$1_$2_$3_$4_$5_$6_$7_$8.txt

sfdp -Tpng -Goverlap=false data/graphdata_$1_sem_$3.dot > data/graphdata_$1_sem_$3.png
sfdp -Tpng -Goverlap=false data/graphdata_$2_sem_$3.dot > data/graphdata_$2_sem_$3.png
sfdp -Tpng -Goverlap=false data/graphdata_$1_etym_$3.dot > data/graphdata_$1_etym_$3.png
sfdp -Tpng -Goverlap=false data/graphdata_$2_etym_$3.dot > data/graphdata_$2_etym_$3.png