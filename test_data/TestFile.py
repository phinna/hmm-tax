import unittest
from qiime.util import get_tmp_filename
from cogent.util.misc import remove_files
from seq import unique_taxonomy_collection
from seq import classify_seqID
from seq import pick_seqID_from_list
from seq import count_same_seq

c_taxonomy_string=\
"""2528843 c__AAG;
2493663 c__Alphaproteobacteria;
822577  c__Alphaproteobacteria;
1837676 c__Alphaproteobacteria;
1928988 c__MBGB;
3770699 c__[Parvarchaea];
229854  c__Gammaproteobacteria;
2335039 c__MHVG;
3779572 c__Chloroplast;
717487  c__Alphaproteobacteria;
"""
class SequenceTest(unittest.TestCase):
    
    
    def setUp(self):
        self.taxonomy_file=get_tmp_filename(\
         prefix='c__taxonomy_',suffix='.txt')

        self._paths_to_clean_up=[self.taxonomy_file]


        open(self.taxonomy_file,'w').write(c_taxonomy_string)


    def tearDown(self):
    	remove_files(set(self._paths_to_clean_up))

    def test_unique_taxonomy_collection(self):
    
        expected=['c__AAG;','c__Alphaproteobacteria;','c__MBGB;','c__[Parvarchaea];',\
	          'c__Gammaproteobacteria;','c__MHVG;','c__Chloroplast;']
    	
	actual=unique_taxonomy_collection(self.taxonomy_file)
        self.assertEqual(actual,expected)

    

    def test_classify_seqID(self):
        
	taxonomy_collection=['c__AAG;','c__Alphaproteobacteria;','c__MBGB;',\
			     'c__[Parvarchaea];','c__Gammaproteobacteria;',\
			     'c__MHVG;','c__Chloroplast;']
	
	expected=[['c__AAG;','2528843'],['c__Alphaproteobacteria;','2493663',\
		   '822577','1837676','717487'],['c__MBGB;','1928988'],\
		  ['c__[Parvarchaea];','3770699'],['c__Gammaproteobacteria;','229854'],\
		  ['c__MHVG;','2335039'], ['c__Chloroplast;','3779572']]

	actual=classify_seqID(self.taxonomy_file,taxonomy_collection)
        self.assertEqual(actual,expected)

    
    def test_pick_seqID_from_list1(self):
	
        tgroup_list=[['c__AAG;','2528843'],['c__Alphaproteobacteria;','2493663',\
		   '822577','1837676','717487'],['c__MBGB;','1928988'],\
		  ['c__[Parvarchaea];','3770699'],['c__Gammaproteobacteria;','229854'],\
		  ['c__MHVG;','2335039'], ['c__Chloroplast;','3779572']]

        utc='c__Alphaproteobacteria;'

        expected=['2493663','822577','1837676','717487']

	actual=pick_seqID_from_list(utc,tgroup_list)
	self.assertEqual(actual,expected)

    def test_count_same_seq(self):
	
	otu_files=['61_otus.fasta']
	identify_number='2493663'
	expected="""ATGCTTAACACATGCAAGTCGAACAATTTGGGGCTATTGGAAGCTCCTAGCTTTGCAGCTTGTCTCTCTCTTTTGATAGGAGACTTTGATAATGAAGTGGCGAACGGGTGCGTAAGGCGTGGGAAATTCTGCCGGAGAGAAAGCTAACGAAGAGCACTCCTTGATGAGCCCGCGTAGTATTAGGTAGTTGGTTAGGTTACGGCTGACCAAGCCGATGATGCTTAGTTGATCTTTTCGGATGATCAGCCACACCGGGACTGAGACAAGGCCCGGACCCAGGATTGGGGCAGCAGTGGGGAATCTTGGACAATAGGCGCCAGCCCGATCCAGCAATCTTGCGTGATTTAGACTCGTAAGGAGCCCGCCGGAGTGCGGGGATCTAGGGCACTTTCGCTTGTAAAAGCTCTTTCAACGAGTATGCGATGATGACATGACTCGTGTAAGAAGCTCCGGCTAACTTCGTGCCAGCAGCCGCGGTAAGACGAAGGGGGCAAGTCTTTCTCGGAATGACTGGGCGTAAAGAGCATGTAGGCGGTCAGTCAAATTGGAGCGGAAAAGCGCCATACAGATGGTGAGGTGTTCCCAATAAGACTGACTTGGGTCAGATAAGGGAGAGTGGAATTTCGTAGGGAGTTGGAAGAACACCTAAATCTATGTAAGGCAGTCCTAAGGCGAAGGCAGCTCTCTAGGTCTATACCGACGCTAAATGTGCGAAAGCGTGGGTAGCAAACAGGATTAGAGACCCTGGTAGTCCACGCTGTCAACGATGAGTGTTAGCTGTTTGGTCGTGTGATCAGGAGCACAGCTAACGCGTGAAACACTCCGCCTGGGGAGTACAGTCGCAAGGCTGAAACTCAAAGGAATTGACGGGGGCCCGCATAAGCGGTGGAGCATGTGGTTTAATTCGATACAACGCGAAAGGATCTTACCAGCCTTTGAATATGAGATCGTAGGCAAGGAGACGGGGGAGTTTGAATAAGGGCCAATTATGATAAGAAGACGCTTCTACCCTAATCGCTCCCTCCAATTATGAAAAGAATGAGATCCCATACCTTTTTTCCTCGCGACTAGCCAGGAGGATGAAGCTTAGTACGCTTTCGTACAGGTGTTGCATGGCTGTCGTCAGTCCGTGTCGTGGGATGTCGGGTCAATTCCTATAACGGGCGAAACCCTTTTTTTGTGTTGCAGAACACGTGTATCCTAGGCTTCGGGATTCTAAGTGGTAATACAGAGGAGTATACCATAACCAGCCCATGAATTAGAGAGGGTGCGCGTCGCACTCACAAGAGACAGACGCTTATATGGTGTAGGAAGGTGGGGATGACGTCAAGTCCGCATGGTCCTTAAAGGCTGGGCCACACACGTGCTACAATGACAATTACAATGGGATGTGAAAACTGCACCCTCAAAGATTGTCGCAGTTCGGATTCCTCTCTGTAATTCGGGAGGATGAAGCAGGAATCGCTAGTAATCGCGGATTAGGATGCCGCGGTGAACTGAGAACCGGGTTTTGTACACACCGCCCGTCACACCCTGGGAATTGGTTTCGCCCTAAGCATCAACGCGGAGGTTGCCCATGACTTGCTTCTGGTTTCTTTGCCATGGAGTGTTCCTTGGCAGTCTTTGTTGGATACCACGGTGGGGTCTCTGACTGGGGTGAAGTCGTAACAAGGTAGCCGTAGGGGA
"""
	actual=count_same_seq(otu_files, identify_number)
	self.assertEqual(actual,expected)


if __name__=='__main__':
    unittest.main()


 
