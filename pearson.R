# Performs the Pearson correlation

# rscript pearson.R

library(tidyverse)

# Working dir must be set to englishConnectome dir

avg_dists <- read_csv("data/avg_distances_noprefix.csv", col_names=TRUE)

avg_dists_1 <- avg_dists[avg_dists$sample < 81, ]
avg_dists_2 <- avg_dists[avg_dists$sample > 80 & avg_dists$sample < 161, ]
avg_dists_3 <- avg_dists[avg_dists$sample > 160 & avg_dists$sample < 241, ]
avg_dists_4 <- avg_dists[avg_dists$sample > 240 & avg_dists$sample < 321, ]
avg_dists_5 <- avg_dists[avg_dists$sample > 320 & avg_dists$sample < 401, ]
avg_dists_6 <- avg_dists[avg_dists$sample > 400 & avg_dists$sample < 481, ]
avg_dists_7 <- avg_dists[avg_dists$sample > 480 & avg_dists$sample < 561, ]
avg_dists_8 <- avg_dists[avg_dists$sample > 560 & avg_dists$sample < 641, ]
avg_dists_9 <- avg_dists[avg_dists$sample > 640 & avg_dists$sample < 721, ]

cat("1-80,",cor(avg_dists_1$sem_avg, avg_dists_1$etym_avg, method="pearson"), "\n")
cat("81-160,",cor(avg_dists_2$sem_avg, avg_dists_2$etym_avg, method="pearson"), "\n")
cat("161-240,",cor(avg_dists_3$sem_avg, avg_dists_3$etym_avg, method="pearson"), "\n")
cat("241-320,",cor(avg_dists_4$sem_avg, avg_dists_4$etym_avg, method="pearson"), "\n")
cat("321-400,",cor(avg_dists_5$sem_avg, avg_dists_5$etym_avg, method="pearson"), "\n")
cat("401-480,",cor(avg_dists_6$sem_avg, avg_dists_6$etym_avg, method="pearson"), "\n")
cat("481-560,",cor(avg_dists_7$sem_avg, avg_dists_7$etym_avg, method="pearson"), "\n")
cat("561-640,",cor(avg_dists_8$sem_avg, avg_dists_8$etym_avg, method="pearson"), "\n")
cat("641-720,",cor(avg_dists_9$sem_avg, avg_dists_9$etym_avg, method="pearson"), "\n")