# Perform distance calculations for run_analysis.sh

# Usage ./calc_distances.sh

# all etym 2500 (1-80)
./analyse_run.sh data/sem_links_nodes_etym_links_nodes_intersected.txt data/sem_links.csv data/etym_links.csv 80 2500 0

# all etym 1000 (81-160)
./analyse_run.sh data/sem_links_nodes_etym_links_nodes_intersected.txt data/sem_links.csv data/etym_links.csv 80 1000 80;

# no roots 2500 (161-240)
./analyse_run.sh data/sem_links_nodes_etym_links_noroots_nodes_intersected.txt data/sem_links.csv data/etym_links_noroots.csv 80 2500 160;

# no roots no affix 1000 (241-320)
./analyse_run.sh data/sem_links_nodes_etym_links_noaffix_noroots_nodes_intersected.txt data/sem_links.csv data/etym_links_noaffix_noroots.csv 80 1000 240;

# only roots 1000 (321-400)
./analyse_run.sh data/sem_links_nodes_etym_links_onlyroots_nodes_intersected.txt data/sem_links.csv data/etym_links_onlyroots.csv 80 1000 320;

# with roots no affix 1000 (401-480)
./analyse_run.sh data/sem_links_nodes_etym_links_noaffix_withroots_nodes_intersected.txt data/sem_links.csv data/etym_links_noaffix_withroots.csv 80 1000 400;

# no roots 1000 (401-480)
./analyse_run.sh data/sem_links_nodes_etym_links_noroots_nodes_intersected.txt data/sem_links.csv data/etym_links_noroots.csv 80 1000 480;

# no roots no affix 2500 (561-640)
./analyse_run.sh data/sem_links_nodes_etym_links_noaffix_noroots_nodes_intersected.txt data/sem_links.csv data/etym_links_noaffix_noroots.csv 80 2500 560;

# with roots no affix 2500 (641-720)
./analyse_run.sh data/sem_links_nodes_etym_links_noaffix_withroots_nodes_intersected.txt data/sem_links.csv data/etym_links_noaffix_withroots.csv 80 2500 640;
