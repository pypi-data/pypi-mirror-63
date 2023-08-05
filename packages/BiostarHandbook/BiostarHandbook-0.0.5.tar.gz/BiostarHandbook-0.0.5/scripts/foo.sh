#!/usr/bin/env bash

set -uex

PATT="'$*'"

# Path to lineage
LINEAGES=taxa/lineages.txt

# Path to blastinfo
BLAST_INFO=blastinfo.txt

echo "$PATT"

# Isolate all taxids where the lineage matches "bat sars"
cat $LINEAGES | grep -i $PATT | cut -f 1 |
    parallel -j 1 "cat $BLAST_INFO | grep {} | grep 'complete genome'" | \
    cut -f 1 -d ' ' |  parallel -j 1 "blastdbcmd -db db/Betacoronavirus -entry {}"
