#!/usr/bin/env python
# File created on 18 Nov 2013
from __future__ import division

__author__ = "AUTHOR_NAME"
__copyright__ = "Copyright 2013, The BiPy project"
__credits__ = ["AUTHOR_NAME"]
__license__ = "GPL"
__version__ = "0.0.0"
__maintainer__ = "AUTHOR_NAME"
__email__ = "AUTHOR_EMAIL"
__status__ = "Development"

import os
import tempfile
import shutil
from collections import defaultdict
from qcli.util import qcli_system_call
from hmmtax.search_hmm import search_HMM,create_temp_test_seq_file
from hmmtax.search_hmm import taxonomy_assignment_to_query_seq
from qcli import (parse_command_line_parameters, 
                  make_option)

script_info = {}
script_info['brief_description'] = "Assign specific taxonomy for each query nucleotide sequence"

script_info['script_description'] = "Search the query 16S rRNA nucleotide sequences against the profile HMMs database and return the specific taxonomy classificaiton of the corresponding query sequences. The profile HMMs database are built from a series of 16S rRNA alignment files, which are in Stockholm format and from gg_13_5_otus database. "

script_info['script_usage'] = [\
("It takes the query nucleotide sequences and the HMM database as input and output the taxonomic classificaiton for each query sequence",
"It accepts any FASTA file as target HMM profiles input. It also accepts EMBL/UniPort text format, and Genbank format. This script takes query DNA nucleotide sequences, whcih can be single or multiple sequences and HMM database as input. In this case, HMM database has to be created from a database, which is a tree structure.",
"%prog -i test_seqs.fasta -b profileHMMs")]

script_info['output_description']=""

script_info['required_options'] = [
 make_option('-i','--input_query_fp',type="existing_filepath",help='the input query sequences filepath'),
 make_option('-b','--input_HMM_fp',type="existing_dirpath",help='the input profile HMMs filepath'),
 make_option('-o','--output_fp',type="new_filepath",
             help='the output file containing classified taxonomy names')
]

script_info['optional_options']=[]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    
    Query_collection=[] 
    rank_collection=[]
    Query_dict=defaultdict(list)
    temp_dir_name=tempfile.mkdtemp(prefix='root_')
    level=0
    for root,dirs,files in os.walk(opts.input_HMM_fp):
        print root
        #print ".................."
        path_to_db=os.path.join(root,'db')
        path_to_result=os.path.join(root,'result.out')
        if level==0:
            stdout,stderr,return_value = qcli_system_call('cmscan -E 1 '+path_to_db+' '+opts.input_query_fp+' > '+path_to_result)
            if return_value != 0:
                print 'Stdout:\n%s\nStderr:%s\n' % (stdout,stderr)
                exit(1)
            HMM_result=open(path_to_result,'U')
            HMM_choice_list,HMM_Query_list,HMM_choice_list_with_ID=search_HMM(HMM_result)
            create_temp_test_seq_file(temp_dir_name,HMM_choice_list_with_ID,open(opts.input_query_fp,'U'))
            rank_collection.extend(HMM_choice_list)
            Query_collection.extend(HMM_Query_list)
            for Query_ID, rank in HMM_choice_list_with_ID:
                Query_dict[Query_ID].append(rank)
        else:
            if os.path.basename(root) in rank_collection:
                path_to_test_seq=os.path.join(temp_dir_name,os.path.basename(root)+'.fasta')
                stdout,stderr,return_value = qcli_system_call('cmscan -E 1 '+path_to_db+' '+path_to_test_seq+' > '+path_to_result)
                if return_value != 0:
                    print 'Stdout:\n%s\nStderr:%s\n' % (stdout,stderr)
                    exit(1)
                HMM_result=open(path_to_result,'U')
                HMM_choice_list,HMM_Query_list,HMM_choice_list_with_ID=search_HMM(HMM_result)
                create_temp_test_seq_file(temp_dir_name,HMM_choice_list_with_ID,open(path_to_test_seq,'U'))
                rank_collection.extend(HMM_choice_list)
                for Query_ID, rank in HMM_choice_list_with_ID:
                    Query_dict[Query_ID].append(rank)
        level+=1
    
    shutil.rmtree(temp_dir_name)
    taxonomy_assignment_to_query_seq(Query_dict,Query_collection,opts.output_fp)

if __name__ == "__main__":
    main()
