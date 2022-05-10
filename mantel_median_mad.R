# Calculates median and MAD for mantel test

# rscript mantel_median_mad.R

library(tidyverse)

cmd_args <- commandArgs(trailingOnly = TRUE)

data_csv <- read_csv(cmd_args[1])

mantel_median <- median(data_csv$signif)

mantel_mad <- mad(data_csv$signif)

cat(mantel_median, ",", mantel_mad, "\n")