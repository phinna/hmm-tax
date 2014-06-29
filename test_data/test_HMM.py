#!/usr/bin/env python
import unittest
import os
import tempfile
from shutil import rmtree
from os.path import exists
from collections import defaultdict
from qiime.util import get_tmp_filename
from cogent.util.misc import remove_files
from tempfile import mkdtemp
from hmmtax.search_hmm import search_HMM
from hmmtax.search_hmm import create_temp_test_seq_file
from hmmtax.search_hmm import taxonomy_assignment_to_query_seq
from hmmtax.assign_seq_to_taxon import build_cm_models
from hmmtax.assign_seq_to_taxon import search_cmfiles_to_cmpress
from hmmtax.assign_seq_to_taxon import cmpress_models
from hmmtax.assign_seq_to_taxon import check_path

query_seq_lines=\
">1000269 HMPMockV1.1.Even2_365838\nTACGTAGGTCCCGAGCGTTGTCCGGATTTATTGGGCGTAAAGCGAGCGCAGGCGGTTAGATAAGTCTGAAGTTAAATACTGTGGCTTAACCATAGTACGCTTTGGAAACCGTTTAACTTGAGTGCAAGAGTGGAGAGTGAAATTCCATGTG\n>1001007 HMPMockV1.2.Staggered1_1181026\nTACGTCGGTGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCCACGGCTCACCCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGT\n"




class HMMTest(unittest.TestCase):
    
    def setUp(self):

    	self.dirs_to_remove = []
	
	self.subSeq_dir=tempfile.mkdtemp(prefix='root_')
	self.querySeq_f=get_tmp_filename(
	    prefix='querySeqTest',suffix='fna')
        self.queryOut_f=get_tmp_filename(
        prefix='queryOutTest',suffix='txt')
       
	self._paths_to_clean_up=\
	    [self.querySeq_f,self.queryOut_f]
        self.dirs_to_remove.append(self.subSeq_dir)        

	querySeq_file=open(self.querySeq_f,'w')
	queryOut_file=open(self.queryOut_f,'w')
	
	querySeq_file.write(query_seq_lines)
	
	querySeq_file.close()
	queryOut_file.close()

    
		
    def tearDown(self):
	
	remove_files(set(self._paths_to_clean_up))
        for d in self.dirs_to_remove:
            if exists(d):
                rmtree(d)
    
    def test_search_HMM(self):
        
        expected_choice,expected_Query,expected_choice_ID=\
            search_HMM(open('/scratch-lt/hhh34/taxonomy_by_infernal_slurm/cmscan_result.out','r'))
        
        actual_Query = ['1000269','1001007']
        actual_choice = ['k__Bacteria','k__Bacteria']
        actual_choice_ID = [('1000269','k__Bacteria'),('1001007','k__Bacteria')]

        self.assertEqual(actual_Query,expected_Query)
        self.assertEqual(actual_choice,expected_choice)
        self.assertEqual(actual_choice_ID,expected_choice_ID)

    def test_create_temp_test_seq_file(self):

        temp_dir_name=self.subSeq_dir
        HMM_choice_ID= [('1000269','k__Bacteria'),('1001007','k__Bacteria')]
        seq_file=open(self.querySeq_f,'r')
        create_temp_test_seq_file(temp_dir_name,HMM_choice_ID, seq_file)

        expected=open(temp_dir_name+'/k__Bacteria.fasta')
        actual=">1000269 HMPMockV1.1.Even2_365838\nTACGTAGGTCCCGAGCGTTGTCCGGATTTATTGGGCGTAAAGCGAGCGCAGGCGGTTAGATAAGTCTGAAGTTAAATACTGTGGCTTAACCATAGTACGCTTTGGAAACCGTTTAACTTGAGTGCAAGAGTGGAGAGTGAAATTCCATGTG\n>1001007 HMPMockV1.2.Staggered1_1181026\nTACGTCGGTGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCCACGGCTCACCCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGT\n"  

        self.assertEqual(actual,expected.read())

    def test_taxonomy_assignment_to_query_seq(self):
        
        Query_collection=['1000269','1001007']
        Query_dict=defaultdict(list)
        Query_dict['1000269'].append('k__Bacteria')
        Query_dict['1001007'].append('k__Bacteria')
        taxonomy_assignment_to_query_seq(Query_dict,Query_collection,self.queryOut_f)

        expected=open(self.queryOut_f)
        actual="1000269\tk__Bacteria\n1001007\tk__Bacteria\n"

        self.assertEqual(actual,expected.read())

    def test_build_cm_models(self):
            
        sto_dir="/scratch-lt/hhh34/test_infernal"
        build_cm_models(sto_dir)
            
            
        expected_cm_list=[]
        for roots,dirs,files in os.walk(sto_dir):
            for name in files:
                fileName,fileExtension = os.path.splitext(name)
                if fileExtension == '.cm':
                    expected_cm_list.append(fileName+'.cm')
        actual=['k__Archaea.cm','k__Bacteria.cm']

        self.assertEqual(actual,expected_cm_list)

    def test_search_cmfiles_to_cmpress(self):
        
        cm_dir="/scratch-lt/hhh34/test_infernal"
        search_cmfiles_to_cmpress(cm_dir)

        expected_cmpress_list=[]
        for roots,dirs,files in os.walk(cm_dir):
            for name in files:
                fileName,fileExtension = os.path.splitext(name)
                if fileExtension == '.i1m':
                    expected_cmpress_list.append(fileName+'.i1m')
        actual=['db.i1m']

        self.assertEqual(actual,expected_cmpress_list)        


    def test_check_path(self):
        
        test_path1="/k__Bacteria/p__f'ekdl"
        test_path2="/k__Bacteria/p__fed sdf"
        test_path3="/k__Bacteria/p_fedsd.sdfsd"

        
        expected_1=check_path(test_path1)
        expected_2=check_path(test_path2)
        expected_3=check_path(test_path3)
        actual_1="/k__Bacteria/p__f\'ekdl"
        actual_2="/k__Bacteria/p__fed sdf"
        actual_3="/k__Bacteria/p_fedsd\.sdfsd"

        self.assertEqual(actual_1,expected_1)
        self.assertEqual(actual_2,expected_2)
        self.assertEqual(actual_3,expected_3)


if __name__=='__main__':
    unittest.main()

