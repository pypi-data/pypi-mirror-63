# -*- coding: utf-8 -*-
#
#   This file is part of the magpurify package, available at:
#   https://github.com/snayfach/MAGpurify
#
#   Magpurify is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.

import argparse
import itertools
import os
import sys
import Bio.Seq
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from magpurify import utilities


def fetch_args(parser):
    parser.set_defaults(func=main)
    parser.set_defaults(program="tetra-freq")
    parser.add_argument("fna", type=str, help="Path to input genome in FASTA format")
    parser.add_argument(
        "out", type=str, help="Output directory to store results and intermediate files",
    )
    parser.add_argument("--cutoff", type=float, default=0.06, help="Cutoff")
    parser.add_argument(
        "--weighted-mean",
        action="store_true",
        help="Compute the mean weighted by the contig length"
    )


def init_kmers():
    tetra = {}
    for i in itertools.product("ACGT", repeat=4):
        kmer_fwd = "".join(i)
        kmer_rev = utilities.reverse_complement(kmer_fwd)
        if kmer_fwd in tetra or kmer_rev in tetra:
            continue
        else:
            tetra[kmer_fwd] = 0
    return tetra


class Contig:
    def __init__(self):
        pass


def main(args):
    utilities.add_tmp_dir(args)
    utilities.check_input(args)
    utilities.check_dependencies(["blastn"])

    print("\u001b[1m" + "• Counting tetranucleotides" + "\u001b[0m")
    # init data
    contigs = {}
    contig_length_list = []
    for id, seq in utilities.parse_fasta(args["fna"]):
        contig = Contig()
        contig.id = id
        contig.seq = str(seq)
        contig.kmers = init_kmers()
        contigs[id] = contig
        contig_length_list.append(len(seq))

    # count kmers
    for contig in contigs.values():
        for i in range(len(contig.seq) - 3):
            kmer_fwd = contig.seq[i : i + 4]
            if kmer_fwd in contig.kmers:
                contig.kmers[kmer_fwd] += 1
            else:
                kmer_rev = utilities.reverse_complement(kmer_fwd)
                contig.kmers[kmer_rev] += 1

    print("\u001b[1m" + "\n• Normalizing counts" + "\u001b[0m")
    for contig in contigs.values():
        total = float(sum(contig.kmers.values()))
        for kmer, count in contig.kmers.items():
            contig.kmers[kmer] = 100 * count / total if total > 0 else 0.0
    print("\u001b[1m" + "\n• Performing PCA" + "\u001b[0m")
    df = pd.DataFrame(dict([(c.id, c.kmers) for c in contigs.values()]))
    pca = PCA(n_components=1)
    pca.fit(df)
    pc1 = pca.components_[0]
    if args["weighted_mean"]:
        print(
            "\u001b[1m"
            + "\n• Computing per-contig deviation from the weighted mean along the first principal component"
            + "\u001b[0m"
        )
        reference_pc = np.average(pc1, weights=contig_length_list)
    else:
        print(
            "\u001b[1m"
            + "\n• Computing per-contig deviation from the mean along the first principal component"
            + "\u001b[0m"
        )
        reference_pc = np.average(pc1)
    for contig_id, contig_pc in zip(list(df.columns), pc1):
        contigs[contig_id].pc = contig_pc
        contigs[contig_id].values = {}
        contigs[contig_id].values["delta"] = abs(contig_pc - reference_pc)

    print("\u001b[1m" + "\n• Identifying outlier contigs" + "\u001b[0m")
    flagged = [
        contig.id
        for contig in contigs.values()
        if contig.values["delta"] > args["cutoff"]
    ]

    out = f"{args['tmp_dir']}/flagged_contigs"
    print(f"  {len(flagged)} flagged contigs: {out}")
    with open(out, "w") as f:
        for contig in flagged:
            f.write(contig + "\n")
