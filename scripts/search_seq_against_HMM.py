import os

def search_HMM(HMM_result):
    """Search query DNA sequences against HMM profiles and \
    return a tuple of query and corresponding taxonomic rank"""
    HMM_choice_list=[]
    HMM_Query_list=[]
    HMM_choice_list_with_ID=[]
    count_line=0
    for line in HMM_result:
        if line.startswith('Query:')==True:
            Query=line.split()[1]
            HMM_Query_list.append(Query)
            count_line=0
        if count_line==5 and line.startswith('#')==False:
            rank=line.lstrip().split()[8]
            if rank in ['k__Bacteria_1','k__Bacteria_2','k__Bacteria_3']:
                rank='k__Bacteria'
            else:
                pass
            HMM_choice_list.append(rank)
            HMM_choice_list_with_ID.append((Query,rank))
        count_line+=1
    
    return HMM_choice_list,HMM_Query_list,HMM_choice_list_with_ID

def create_temp_test_seq_file(temp_dir_name,HMM_choice_list_with_ID,test_seq_file):
    for line in test_seq_file:
        
        for tuple_element in HMM_choice_list_with_ID:
            if line.lstrip('>').rstrip('\n')==tuple_element[0]:
                path_to_test_seq=os.path.join(temp_dir_name,tuple_element[1]+'.fasta')
            else:
                pass
        f=open(path_to_test_seq,'a')
        f.write(line)
        f.close()
    
def taxonomy_assignment_to_query_seq(Query_dict,Query_collection):
    
    f=open('./Query_taxonomy.txt','a')
    for query in Query_collection:
        taxonomy=Query_dict[query]
        t_string=';'.join(taxonomy)
        #f=open('./Query_taxonomy.txt','a')
        f.write(query+'\t'+t_string+'\n')
    f.close()
