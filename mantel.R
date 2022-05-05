# Performs the Pearson correlation

# rscript mantel.R

# install.packages("vegan")

library(tidyverse)

library(vegan)

cmd_args <- commandArgs(trailingOnly = TRUE)

matrix_csv_sem <- read_csv(cmd_args[1], col_names=FALSE)

data_mat_sem <-as.matrix(matrix_csv_sem)


matrix_csv_etym <- read_csv(cmd_args[2], col_names=FALSE)

data_mat_etym <- as.matrix(matrix_csv_etym)

mantel_data <- mantel(data_mat_sem, data_mat_etym, method="pearson", permutations=1000, strata = NULL, na.rm = FALSE, parallel = 8)

cat(mantel_data$signif, ",", mantel_data$statistic, "\n")