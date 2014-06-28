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
from hmmtax.assign_seq_to_taxon import search_cmfile_to_cmpress
from qcli import qcli_system_call
from qcli import (parse_command_line_parameters, 
                  make_option)



script_info = {}

script_info['brief_description'] = "Look for .cm files and cmpress them"

script_info['script_description'] = "Before building the profile HMM on each file, each .cm file is needed to perform the cmpress command "

script_info['script_usage'] = [\
("Takes the directory containing .cm files as input",
  "%prog -i ~/Desktop/fasta_by_taxonomy"),
]

script_info['required_options'] = [
 make_option('-i','--input_dir',type="existing_dirpath",
             help='Input the fasta_by_taxonomy directory')
]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    
    search_cmfile_to_cmpress(opts.input_dir)

if __name__ == "__main__":
    main()
