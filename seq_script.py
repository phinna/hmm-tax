#!/usr/bin/env python
# File created on 24 Jun 2013
from __future__ import division

__author__ = "Huanhua Huang"
__copyright__ = "Copyright 2013, The BiPy project"
__credits__ = ["Huanhua Huang"]
__license__ = "GPL"
__version__ = "0.0.0"
__maintainer__ = "Huanhua Huang"
__email__ = "hhh34@nau.edu"
__status__ = "Development"

from data.classify import seperate_taxonomy_list
#ifrom  data import assign_taxonomy
from qcli import (parse_command_line_parameters, 
                  make_option)


taxonomy_levels=['1','2','3','4','5','6','7']

script_info = {}
script_info['brief_description'] = "Split taxonomy and match sequence ID to its corresponding nucleotide sequence at specific taxonomy level"
script_info['script_description'] = "This script split taxonomy into different taxonomy levels and match sequence ID to its corresponding nucleotide sequence at specified taxonomy level. The output file shows the sequence ID and its nucleotide sequence at specific taxonomy level under its own taxonomy directory "
script_info['script_usage'] = [\
("Split taxonomy and match destinctive sequence ID to its corresponding nucleotide sequence at specified taxonomy level in one file.",
 "Split taxonomy in one taxonomy file and match destinctive sequence ID to its corresponding nucleotide sequence based on a fasta file, which corresponds to its taxonom  y file at specified taxonomy level, like phylum level.  Write the results to each t  axonomy file based on their characteristics",
  "%prog -t ./gg_12_10_otus/taxonomy/61_otu_taxonomy.txt -f ./gg_12_10_otus/rep_set/61_otus.fasta -l 6_-o IDseq"),
("Split taxonomy and match destinctive sequence ID to its corresponding nucleotide sequence at specified taxonomy level in two files.",
 "Split taxonomy in two taxonomy files and match destinctive sequence ID to its corresponding nucleotide sequence based on two fasta files, which correspond to their taxonomy files  at specified taxonomy level, like phylum taxonomy level. Write the results to each taxonomy file based on their characteristics.",
"%prog -t ./gg_12_10_otus/taxonomy/61_otu_taxonomy.txt,./gg_12_10_otus/taxonomy/64_otu_taxonomy.txt -f ./gg_12_10_otus/rep_set/61_otus.fasta,./gg_12_10_otus/rep_set/64_otus.fasta -o IDseq"),
("Split taxonomy and match destinctive sequence ID to its corresponding nucleotide sequence at specified taxonomy level in more than two files.",
"Split taxonomy in more than two taxonomy files and match destinctive sequence ID to its corresponding nucleotide sequence based on more than two fasta file, which correspond to their taxonomy file at specified taxonomy level, like phylum taxonomy level. Write the results to each taxonomy file based on their characteristics",
"%prog -t \"./gg_12_10_otus/taxonomy/*.txt\" -f \"./gg_12_10_otus/rep_set/*.fasta\" -o IDseq")]
script_info['output_description']= "The sequence ID and its nucleotide sequence at specified taxonomy level is written to its specific taxonomy file"
script_info['required_options'] = [
 make_option('-t','--input_taxonomy_fps',type="existing_filepaths",
             help='Input taxonomy files containing seqID and'+\
                   'its corresponding taxonomies'),
 make_option('-f','--input_fasta_fps',type="existing_filepaths",
             help='Input fasta files, which correspond its taxonomy files'),
 make_option('-l','--taxonomy_level',type="choice",
             help='Split input files at the specific taxonomy level.'
                  ' Valid taxonomy levels are:'+\
                   ','.join(taxonomy_levels)+'[default: %default]',
                   choices=taxonomy_levels, default='7'),
 make_option('-o','--output_dir',type="new_dirpath",
             help='the output directory containing classified taxonomy directories')
]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    
    sub_taxonomy_list=[]
    if opts.taxonomy_level=="":
        sub_taxonomy=seperate_taxonomy_list(opts.input_taxonomy_fps,'7')
        sub_taxonomy_list.append(sub_taxonomy)
        assign_seqID_to_seqs(sub_taxonomy_list,opts.input_fasta_fps,opts.output_dir)
    else:
        sub_taxonomy=seperate_taxonomy_list(opts.input_taxonomy_fps,opts.taxonomy_level)
        sub_taxonomy_list.append(sub_taxonomy)
        assign_seqID_to_seqs(sub_taxonomy_list,opts.input_fasta_fps,opts.output_dir)
  

if __name__ == "__main__":
    main()
