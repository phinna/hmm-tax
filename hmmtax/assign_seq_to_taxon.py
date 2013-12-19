#!/usr/bin/env python
##################################################
# Topic: Match each otu ID to its                #
#	 corresponding nucleotide sequence       #
#                                                #
##################################################
import os
import subprocess
from qcli import qcli_system_call

def unique_taxa_collection_at_the_level(taxonomy_file):    
    """
    Filter repeated otu IDs in a taxonomy file which is at a specified taxonomic level and return a list of a unique taxonomy collection.
    """  
    t_collection_at_the_level=[]
    for line in taxonomy_file:
        if line=="":
            break
    	else:
            ID=line.split('\t')[0]
            name=line.split('\t')[1]
            if name in ['k__;\n','p__;\n','o__;\n','c__;\n',
                        'f__;\n','g__;\n','s__\n']:
                pass
            else:
                name=name.rstrip(';\n')
                t_collection_at_the_level.append(name)
    t_collection_at_the_level=list(set(t_collection_at_the_level))
    #print t_collection_at_the_level
    return t_collection_at_the_level
	
def classify_otuID(taxonomy_collection,splitted_taxonomy_file):
    """
    Classify otu IDs based on each taxonomy at a specified taxonomy level and return a list which conains otu IDs and the corresponding taxonomy.
    """
    name_list=[]
    ID_list=[]
    for line in splitted_taxonomy_file:
        ID_name=line.split('\t')
        if ID_name[1].strip(';\n') in taxonomy_collection:
            name_list.append(ID_name[1].strip(';\n'))
            ID_list.append(ID_name[0])
    zipped=list(set(zip(name_list,ID_list)))
    #print zipped
    new_t_collection=[]
    for tuple_element in zipped:
        if tuple_element[0] not in new_t_collection:
            new_t_collection.append(tuple_element[0])
            sublist=[]
            new_t_collection.append(sublist)
            sublist.append(tuple_element[0])
            sublist.append(tuple_element[1])
        else:
            for list_element in new_t_collection:
                if type(list_element)==list:
                    if tuple_element[0]==list_element[0]:
                        list_element.append(tuple_element[1])
                    else:
                        pass
                else:
                    pass
    for t_string in new_t_collection:
        if type(t_string)==str:
            new_t_collection.remove(t_string) 
    print new_t_collection
    return new_t_collection

def pick_seq(otu_files, identify_number):
    """
    Return a nucleotide sequence which corresponds to the otu ID passed in this function.
    """
    for i in range(len(otu_files)):
        f2=open(otu_files[i])
        while 1:
    	    DNAline=f2.readline()
            if (DNAline.find('>')==0):
                ID=DNAline.lstrip('>')
                newID=ID.rstrip('\n')
                if identify_number==newID:
                    print identify_number 
                    break
                else:
                    continue
    	    elif DNAline=='':
                break
    	    else:
                continue
        nucleotide_seq=f2.readline()
        break	
    f2.close()    
    print nucleotide_seq
    return nucleotide_seq

def pick_otuID_from_list(taxonomy,tgroup_list):
    """
    Pick and return a otu ID from a list which contains a sequence of otu IDs under    a specified taxonomy group.
    """
    otuID=[]
    for n in range(0,len(tgroup_list)):
        if taxonomy==tgroup_list[n][0]:
            for j in range(1,len(tgroup_list[n])):
                otuID.append(tgroup_list[n][j])
            break
        else:
            continue
    return otuID

def at_fasta_file(ID_NucleoSeq,output_fp):
    """
    Write the otu ID and its corresponding nucleotide sequence into a .fasta file. 
    """
    if len(ID_NucleoSeq)!=0:
        output_f=open(output_fp,'w')
        for i in range(0,len(ID_NucleoSeq)):
            if (i%2)==0:
                output_f.write('>'+ID_NucleoSeq[i]+'\n')
            else:
                output_f.write(ID_NucleoSeq[i]+'\n')
        output_f.close()

def generate_sto_file(ID_NucleoSeq,output_fp):
    """
    Create a sto file with otu ID and its nucleotide sequence.
    """
    if len(ID_NucleoSeq)!=0:
        output_f=open(output_fp,'w')
        output_f.write('# STOCKHOLM 1.0\n\n')
        for i in range(0,len(ID_NucleoSeq)):
            if (i%2)==0:
                output_f.write('>'+ID_NucleoSeq[i]+'\t')
            else:
                output_f.write(ID_NucleoSeq[i]+'\n')
        output_f.write('//\n')
        output_f.close()

def search_root(dictionary,output_dir,predecessor):
    taxa_strings=[]
    if predecessor == output_dir:
        taxa_strings.append(output_dir)
    else:
        while 1:
            if predecessor in ['k__Archaea;','k__Bacteria;','Wrong_taxa']:
                taxa_strings.append(predecessor)
                taxa_strings.append(output_dir+';')
                break
            else:
                taxa_strings.append(predecessor)
                predecessor=dictionary[predecessor]
    return taxa_strings

def search_dictionary(taxonomy_file,dictionary,search_t):
    if taxonomy_file == 's_taxonomy.txt':
        search_t=search_t.rstrip(';')
        try: 
            predecessor=dictionary[search_t]
        except KeyError:
            search_t=search_t+';'
            predecessor=dictionary[search_t]
    else:
        try: 
            predecessor=dictionary[search_t]
        except KeyError:
            print "Oops! KeyError:",search_t
            predecessor='Wrong_taxa'
    return predecessor

def taxa_strings_to_path(taxa_strings):
    result=[]
    for taxa_string in reversed(taxa_strings):
        result.append(taxa_string.strip(';'))
    return os.path.join(*result)     

def build_hmm_models(level,output_dir):
    for roots,dirs,files in os.walk('../scripts/'+output_dir):
        #print roots
        #print dirs
        #print files
        #print '===================================='
        path_to_sto_list=[]
        path_to_hmm_list=[]
        path_to_dir=[]
        db_exist=[]
        for name in dirs:
            path_to_dir.append(os.path.join(roots,name))
        for name in files:
            fileName, fileExtension = os.path.splitext(name)
            if fileExtension=='.sto':
                path_to_sto_list.append(os.path.join(roots,name))
                path_to_hmm_list.append(os.path.join(roots,fileName+'.hmm'))
            elif fileName=='db':
                db_exist.append('True')
        path_to_hmm_db=os.path.join(roots,'db')
        if db_exist!=[]:
            del db_exist[0]
            #pass
        elif (db_exist==[] and path_to_sto_list!=[]):
            for i in range(len(path_to_sto_list)):
                #subprocess.call(['hmmbuild',path_to_hmm_list[i],path_to_sto_list[i]])
                stdout,stderr,return_value = qcli_system_call('hmmbuild '+path_to_hmm_list[i]+' '+path_to_sto_list[i])
                if return_value != 0:
                    print 'Stdout:\n%s\nStderr:%s\n' % (stdout,stderr)
                    exit(1)
            content=[]
            for i in range(len(path_to_hmm_list)):
                try:
                    f=open(path_to_hmm_list[i],'U')
                    content.append(f.read())
                    f.close()
                except IOError:
                    print path_to_hmm_list[i]
            f=open(path_to_hmm_db,'w')
            for i in range(len(path_to_hmm_list)):
                f.write(content[i])
            f.close()
            subprocess.call(['hmmpress',path_to_hmm_db])
        else:
            pass
           	
 
def assign_otuID_to_seqs(dictionary,taxonomy_fps,taxonomy_files,otu_files,output_dir): 

    for tf in taxonomy_files:
        path_to_splitted_taxonomy_file=os.path.join(output_dir,tf)
        utc1=unique_taxa_collection_at_the_level(open(path_to_splitted_taxonomy_file,'U'))
        tgroup_list=classify_otuID(utc1,open(path_to_splitted_taxonomy_file,'U'))
        for taxa_name in utc1:
            otuID_list=pick_otuID_from_list(taxa_name,tgroup_list)
            ID_NucleoSeq=[]
            for otuID in otuID_list:
                nucleotide_seq=pick_seq(otu_files, otuID)
                if nucleotide_seq!='':
                    ID_NucleoSeq.append(otuID)
                    ID_NucleoSeq.append(nucleotide_seq)
                else:
                    continue
            
            if taxa_name=='k__Bacteria':
                predecessor=output_dir
            elif taxa_name=='k__Archaea':
                predecessor=output_dir
            else:
                predecessor=search_dictionary(tf,dictionary,taxa_name+';') 
            
            taxonomy_strings=search_root(dictionary,output_dir,predecessor)
            path_to_output_dir=taxa_strings_to_path(taxonomy_strings)
            if ID_NucleoSeq==[]:
                pass
            else:
                if os.path.exists(path_to_output_dir) == False:
                    os.makedirs(path_to_output_dir,0755)
                else:
                    pass
                output_taxonomy_fp=os.path.join(path_to_output_dir,taxa_name+'.fasta')
                at_fasta_file(ID_NucleoSeq,output_taxonomy_fp)
                output_sto_fp=os.path.join(path_to_output_dir,taxa_name+'.sto')
                generate_sto_file(ID_NucleoSeq,output_sto_fp)
            


def main():
    
    taxonomy_files=['c_taxonomy.txt','f_taxonomy.txt','g_taxonomy.txt',
                    'k_taxonomy.txt','o_taxonomy.txt','p_taxonomy.txt','s_taxonomy.txt']
    otu_files=['61_otus.fasta','64_otus.fasta','67_otus.fasta','70_otus.fasta',
               '73_otus.fasta','76_otus.fasta','79_otus.fasta','82_otus.fasta',
               '85_otus.fasta','88_otus.fasta','91_otus.fasta','94_otus.fasta',
               '97_otus.fasta','99_otus.fasta']
    assign_otuID_to_seqs(taxonomy_files,otu_files,output_dir) 
  
if __name__=="__main__":
    main()


