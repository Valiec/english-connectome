# Derivation and Meaning: A Computer-Assisted Investigation into Etymological and Semantic Connections in English

![Linguistic connectome icon](https://raw.githubusercontent.com/Valiec/english-connectome/main/figdata/Side-by-side_512.png)

An important subfield within philology is etymology, the study of words and their origins. This thesis combines philology and etymology with computational techniques to quantify the large-scale relationships between words in the English language. Specifically, using English headwords, definitions, and etymology data from Wiktionary, graphs were constructed of English words and their relationships in etymology and meaning. These graphs were then examined to test for any correlation between etymological and semantic associations in the graphs. No clear correlation was found, meaning relationships in etymology are not a reliable guide to relationships in meaning in the English language. 

This repository contains scripts and tools for investigating etymological and semantic links in the English linguistic connectome.

## How to use
To run the main analysis described in the paper and produce the 720 mean etymological and semantic distances, run `./run_analysis.sh` 

To run any other analysis, check the relevant script files for a header comment explaining their purpose and arguments.
