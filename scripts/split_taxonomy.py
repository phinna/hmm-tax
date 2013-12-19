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

from os import mkdir,path
from hmmtax.split_taxonomy import split_taxonomy_list
from hmmtax.split_taxonomy import create_dictionary
from hmmtax.assign_seq_to_taxon import assign_otuID_to_seqs
from hmmtax.assign_seq_to_taxon import  build_hmm_models
from qcli import qcli_system_call
from qcli import (parse_command_line_parameters, 
                  make_option)


taxonomy_levels=['1','2','3','4','5','6','7']

script_info = {}
script_info['brief_description'] = "Split taxonomy by level and match the otu ID to the corresponding nucleotide sequence at each specific taxonomy level"
script_info['script_description'] = "This script splits taxonomy into different taxonomy levels and matches the otu ID to its corresponding nucleotide sequence at a specified taxonomic level. The output file contains the sequence ID and its nucleotide sequence at a specific taxonomy level under its own taxonomy directory "
script_info['script_usage'] = [\
("Split taxonomy and match the distinct otu ID to its corresponding nucleotide sequence at a specified taxonomy level in one file.",
 "Split taxonomy in a taxonomy file and match the distinct otu ID to its corresponding nucleotide sequence based on the fasta file, which corresponds to the taxonomy file at a specified taxonomy level, which is indicated by numbers 1, 2, 3..., for instance: to split on phylum level pass 6 in the option.  Write the results to each taxonomy file based on each otu level",
  "%prog -t ./gg_12_10_otus/taxonomy/61_otu_taxonomy.txt -f ./gg_12_10_otus/rep_set/61_otus.fasta -l 6_-o IDseq"),
("Split taxonomy and match distinct otu ID to its corresponding nucleotide sequence at a specified taxonomy level in two files.",
 "Split taxonomy in two taxonomy files and match distinct otu ID to its corresponding nucleotide sequence based on two fasta files, which correspond to the taxonomy files  at a specified taxonomy level, which is indicated by numbers 1, 2, 3..., for instance: to split on phylum level pass 6 in the option. Write the results to each taxonomy file based on each otu level.",
"%prog -t ./gg_12_10_otus/taxonomy/61_otu_taxonomy.txt,./gg_12_10_otus/taxonomy/64_otu_taxonomy.txt -f ./gg_12_10_otus/rep_set/61_otus.fasta,./gg_12_10_otus/rep_set/64_otus.fasta -o IDseq"),
("Split taxonomy and match distinct otu ID to its corresponding nucleotide sequence at a specified taxonomy level in more than two files.",
"Split taxonomy in more than two taxonomy files and match distinct otu ID to its corresponding nucleotide sequence based on more than two fasta file, which correspond to their taxonomy file at a specified taxonomy level, which is indicated by numbers 1, 2, 3..., for instance: to split on phylum level pass 6 in the option. Write the results to each taxonomy file based on each otu level",
"%prog -t \"./gg_12_10_otus/taxonomy/*.txt\" -f \"./gg_12_10_otus/rep_set/*.fasta\" -o IDseq")]
script_info['output_description']= "The sequence ID and its nucleotide sequence at specified taxonomy level is written to its specific taxonomy file"
script_info['required_options'] = [
 make_option('-t','--input_taxonomy_fps',type="existing_filepaths",
             help='Input taxonomy files containing otuID and'+\
                   'its corresponding taxonomies'),
 make_option('-f','--input_fasta_fps',type="existing_filepaths",
             help='Input fasta files, which correspond its taxonomy files'),
 make_option('-l','--taxonomy_level',type='int',
             help='Split input files at the specific taxonomy level.'
                  ' Valid taxonomy levels are:'+\
                   ','.join(taxonomy_levels)+'[default: %default]',
                   default=7),
 make_option('-o','--output_dir',type="new_dirpath",
             help='the output directory containing classified taxonomy directories')
]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
     
    sub_taxonomy_list=[]
    dictionary=create_dictionary(opts.input_taxonomy_fps)
    if opts.taxonomy_level=="":
        if path.isdir(opts.output_dir)==False:
            mkdir(opts.output_dir,0755)
            sub_taxonomy=split_taxonomy_list(opts.input_taxonomy_fps,7,opts.output_dir)
            sub_taxonomy_list.append(sub_taxonomy)
            assign_otuID_to_seqs(dictionary,sub_taxonomy_list,opts.input_fasta_fps,opts.output_dir)
        else:
            sub_taxonomy=split_taxonomy_list(opts.input_taxonomy_fps,7,opts.output_dir)
            sub_taxonomy_list.append(sub_taxonomy)
            assign_otuID_to_seqs(dictionary,sub_taxonomy_list,opts.input_fasta_fps,opts.output_dir)
    else:
        if path.isdir(opts.output_dir)==False:
            mkdir(opts.output_dir,0755)
            sub_taxonomy=split_taxonomy_list(opts.input_taxonomy_fps,opts.taxonomy_level,opts.output_dir)
            sub_taxonomy_list.append(sub_taxonomy)
            assign_otuID_to_seqs(dictionary,opts.input_taxonomy_fps,sub_taxonomy_list,opts.input_fasta_fps,opts.output_dir)
        else:
            sub_taxonomy=split_taxonomy_list(opts.input_taxonomy_fps,opts.taxonomy_level,opts.output_dir)
            sub_taxonomy_list.append(sub_taxonomy)
            assign_otuID_to_seqs(dictionary,opts.input_taxonomy_fps,sub_taxonomy_list,opts.input_fasta_fps,opts.output_dir)
 
    build_hmm_models(opts.taxonomy_level,opts.output_dir)

if __name__ == "__main__":
    main()
