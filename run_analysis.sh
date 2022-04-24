python3 sem_links.py rawData/words.txt;

python3 etym_links.py rawData/etymology.csv -;
python3 etym_links.py rawData/etymology.csv noroots exclude has_root;
python3 etym_links.py rawData/etymology.csv onlyroots include has_root;
python3 etym_links.py rawData/etymology.csv noaffix_noroots exclude has_prefix has_prefix_with_root has_suffix has_suffix_with_root has_confix has_affix compound_of has_root;
python3 etym_links.py rawData/etymology.csv noaffix_withroots exclude has_prefix has_prefix_with_root has_suffix has_suffix_with_root has_confix has_affix compound_of;

python3 get_nodes.py data/sem_links.csv;
python3 get_nodes.py data/etym_links.csv;
python3 get_nodes.py data/etym_links_noroots.csv;
python3 get_nodes.py data/etym_links_onlyroots.csv;
python3 get_nodes.py data/etym_links_noaffix_noroots.csv;
python3 get_nodes.py data/etym_links_noaffix_withroots.csv;

python3 intersect.py data/sem_links.csv data/etym_links.csv;
python3 intersect.py data/sem_links.csv data/etym_links_noroots.csv;
python3 intersect.py data/sem_links.csv data/etym_links_onlyroots.csv;
python3 intersect.py data/sem_links.csv data/etym_links_noaffix_noroots.csv;
python3 intersect.py data/sem_links.csv data/etym_links_noaffix_withroots.csv;

./calc_distances.sh;

./average.sh 1 720 avg_distances;

python3 graph_avgs.py data/avg_distances.csv;