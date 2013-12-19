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
from search_seq_against_HMM import search_HMM,create_temp_test_seq_file
from search_seq_against_HMM import taxonomy_assignment_to_query_seq
from qcli import (parse_command_line_parameters, 
                  make_option)

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = []
script_info['script_usage'].append(("","",""))
script_info['output_description']= ""
script_info['required_options'] = [
 # Example required option
 #make_option('-i','--input_fp',type="existing_filepath",help='the input filepath'),
]
script_info['optional_options'] = [
 # Example optional option
 #make_option('-o','--output_dir',type="new_dirpath",help='the output directory [default: %default]'),
]
script_info['version'] = __version__



def main():
    #option_parser, opts, args =\
     #  parse_command_line_parameters(**script_info)
    Query_collection=[] 
    rank_collection=[]
    Query_dict=defaultdict(list)
    temp_dir_name=tempfile.mkdtemp(prefix='root_')
    level=0
    for root,dirs,files in os.walk('./fasta_by_taxonomy2'):
        #print root
        #print dirs
        #print files
        #print ".................."
        path_to_db=os.path.join(root,'db')
        path_to_result=os.path.join(root,'result.out')
        if level==0:
            stdout,stderr,return_value = qcli_system_call('hmmscan '+path_to_db+' ./test_seqs.fasta > '+path_to_result)
            if return_value != 0:
                print 'Stdout:\n%s\nStderr:%s\n' % (stdout,stderr)
                exit(1)
            HMM_result=open(path_to_result,'U')
            HMM_choice_list,HMM_Query_list,HMM_choice_list_with_ID=search_HMM(HMM_result)
            create_temp_test_seq_file(temp_dir_name,HMM_choice_list_with_ID,open('./test_seqs.fasta','U'))
            rank_collection.extend(HMM_choice_list)
            Query_collection.extend(HMM_Query_list)
            for Query_ID, rank in HMM_choice_list_with_ID:
                Query_dict[Query_ID].append(rank)
        else:
            if os.path.basename(root) in rank_collection:
                path_to_test_seq=os.path.join(temp_dir_name,os.path.basename(root)+'.fasta')
                stdout,stderr,return_value = qcli_system_call('hmmscan '+path_to_db+' '+path_to_test_seq+' > '+path_to_result)
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
    print Query_dict.items()
    shutil.rmtree(temp_dir_name)
    taxonomy_assignment_to_query_seq(Query_dict,Query_collection)
if __name__ == "__main__":
    main()
