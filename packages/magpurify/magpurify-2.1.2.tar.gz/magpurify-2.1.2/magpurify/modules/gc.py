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
import os
import sys
import numpy as np
from Bio import SeqUtils
from magpurify import utilities


def fetch_args(parser):
    parser.set_defaults(func=main)
    parser.set_defaults(program="gc-content")
    parser.add_argument(
        "fna",
        type=str,
        help="Path to input genome in FASTA format"
    )
    parser.add_argument(
        "out",
        type=str,
        help="Output directory to store results and intermediate files",
    )
    parser.add_argument(
        "--cutoff", type=float, default=15.75, help="Cutoff"
    )
    parser.add_argument(
        "--weighted-mean",
        action="store_true",
        help="Compute the mean weighted by the contig length"
    )


class Contig:
    def __init__(self):
        pass


def main(args):
    utilities.add_tmp_dir(args)
    utilities.check_input(args)
    if args["weighted_mean"]:
        print("\u001b[1m" + "• Computing weighted mean contig GC content" + "\u001b[0m")
    else:
        print("\u001b[1m" + "• Computing mean contig GC content" + "\u001b[0m")
    contigs = {}
    contig_length_list = []
    for id, seq in utilities.parse_fasta(args["fna"]):
        contig = Contig()
        contig.id = id
        contig.seq = str(seq)
        contig.gc = round(SeqUtils.GC(seq), 2)
        contigs[id] = contig
        contig_length_list.append(len(seq))
    if args["weighted_mean"]:
        print("\u001b[1m" + "\n• Computing per-contig deviation from weighted mean" + "\u001b[0m")
        reference = np.average([c.gc for c in contigs.values()], weights=contig_length_list)
    else:
        print("\u001b[1m" + "\n• Computing per-contig deviation from mean" + "\u001b[0m")
        reference = np.average([c.gc for c in contigs.values()])
    for contig in contigs.values():
        contig.values = {}
        contig.values["delta"] = abs(contig.gc - reference)
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
