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

from seq_0719 import assign_seqID_to_seqs
from qcli import (parse_command_line_parameters, 
                  make_option)

script_info = {}
script_info['brief_description'] = "Match each sequence ID to its corresponding nucleotide sequence for each sub-taxonomy"
script_info['script_description'] = "This script classifies seqID based on each sub-taxonomy. Then, the correspondng nucleotide sequence will be picked for each seqID. The output file will show the seqID and its nucleotide sequence in different sub-taxonomy file under its own taxonomy directory"
script_info['script_usage'] = [\
("Match destinctive sequence ID to its corresponding nucleotide sequence for each distinctive taxonomy in one file.",
"Match destinctive sequence ID to its corresponding nucleotide sequence for each distinctive sub-taxonomy in one taxonomy file, which includes all sub-taxonomies found by scientists  and write the results to its sub-taxonomy file, which are under its corresponding taxonomic rank directory",
"%prog -i c_taxonomy.txt -o IDseq"),
("Match destinctive sequence ID to its corresponding nucleotide sequence for each distinctive taxonomy in two different files",
"Match destinctive sequence ID to its corresponding nucleotide sequence for each distinctive sub-taxonomy in two taxonomy files, which inlcude all sub-taxonomies found by scientists and write the results to its sub-taxonomy file under its corresponding taxonomic rank directory",
"%prog -i c_taxonomy.txt,f_taxonomy.txt -o IDseq"),
("Match destinctive sequence ID to its corresponding nucleotide sequence for each distinctive sub-taxonomy in many files",
"Match destinctive sequence ID to its corresponding nucleotide sequence for each distinctive sub-taxonomy in many taxonomy files, which include all sub-taxonomies found by scientists and write the results to its sub-taxonomy file under its corresponding taxonomic rank directory",
"%prog -i \"*.txt\" -o IDseq")]
script_info['output_description']= "The sequence ID and its nucleotide sequence for each sub-taxonomy is written to its specific sub-taxonomy file"
script_info['required_options'] = [
 make_option('-i','--input_fps',type="existing_filepaths",help='Input taxonomy files containing seqID and its corresponding taxonomies'),
 make_option('-o','--output_dir',type="new_dirpath",help='the output directory containing classified taxonomy directories')
]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    
    otu_files=['61_otus.fasta','64_otus.fasta','67_otus.fasta','70_otus.fasta',
	       '73_otus.fasta','76_otus.fasta','79_otus.fasta','82_otus.fasta',                '85_otus.fasta','88_otus.fasta','91_otus.fasta','94_otus.fasta',
               '97_otus.fasta']    
 
    assign_seqID_to_seqs(opts.input_fps,otu_files,opts.output_dir)
  

if __name__ == "__main__":
    main()
