##################################################
# Topic: Match each sequence ID to its           #
#	 corresponding nucleotide sequence       #
#                                                #
##################################################
def unique_taxonomy_collection(taxonomy_file):    
   
    f1=open(taxonomy_file)
    
    taxonomy_collection=[]
    
    for taxonomy in f1:
        ID=taxonomy.split()[0]
        name=taxonomy.split()[1]
        count=0
        for i in taxonomy_collection:
	    if i==name:
	        count+=1 
        if count==0:
            taxonomy_collection.append(name)
    
    f1.close()
    
    return taxonomy_collection
	
def classify_seqID(taxonomy_file,taxonomy_collection):
    f1=open(taxonomy_file)
    for taxonomy in f1:
        ID_name=taxonomy.split()
        n=0
        for element in taxonomy_collection:
	    if type(element)==list:
	       if element[0]==ID_name[1]:
		    count=0
		    for i in element:
		        if i==ID_name[0]:
			    count+=1 
		        else:
		            continue
		    if count==0:
		        taxonomy_collection[n].append(ID_name[0])
		        break
		    else:
		        break
	       else:
	           n+=1
	           continue	        
	    elif element==ID_name[1]:
	        taxonomy_collection[n]=[]
	        taxonomy_collection[n].append(ID_name[1])
	        taxonomy_collection[n].append(ID_name[0])
	        break
	    else:
	        n+=1
	        continue
    
    return taxonomy_collection


def count_same_seq(otu_files, identify_number):
    for i in range(len(otu_files)):
	file_path='./gg_12_10_otus/rep_set/otu_file'
	file_path=file_path.replace('otu_file',otu_files[i])
        f2=open(file_path)
	while 1:
    	    DNAline=f2.readline()
            if (DNAline.find('>')==0):
        	ID=DNAline.lstrip('>')
		newID=ID.rstrip()
	        if identify_number==newID: 
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
    return nucleotide_seq



def pick_seqID_from_list(taxonomy,tgroup_list):
    seqID=[]
    for n in range(0,len(tgroup_list)):
        if taxonomy==tgroup_list[n][0]:
	    for j in range(1,len(tgroup_list[n])):
		 seqID.append(tgroup_list[n][j])
	    break
        else:
	    continue
    return seqID


taxonomy_files=['c_taxonomy.txt','f_taxonomy.txt','g_taxonomy.txt','k_taxonomy.txt',
 'o_taxonomy.txt','p_taxonomy.txt','s_taxonomy.txt']
otu_files=['61_otus.fasta','64_otus.fasta','67_otus.fasta','70_otus.fasta',
           '73_otus.fasta','76_otus.fasta','79_otus.fasta','82_otus.fasta',
           '85_otus.fasta','88_otus.fasta','91_otus.fasta','94_otus.fasta',
           '97_otus.fasta','99_otus.fasta']


for tf in taxonomy_files:   
    utc=unique_taxonomy_collection(tf)
    utc1=unique_taxonomy_collection(tf)	
    tgroup_list=classify_seqID(tf,utc)
    tf_dir=tf.rstrip('.txt')
    for i in utc1:
	taxonomy_name=i.rstrip(';')
	seqID_list=pick_seqID_from_list(i,tgroup_list)
	ID_NucleoSeq=[]
        for seqID in seqID_list:
	    nucleotide_seq=count_same_seq(otu_files, seqID)
	    if nucleotide_seq!='':
	        ID_NucleoSeq.append(seqID)
		ID_NucleoSeq.append(nucleotide_seq)
	    else:
		continue
        if len(ID_NucleoSeq)!=0:
	    f=open('./newseq1/'+tf_dir+'/'+taxonomy_name+'.fasta','a')
	    for i in range(0,len(ID_NucleoSeq)):
		if (i%2)==0:
		    f.write('>'+ID_NucleoSeq[i]+'\n')
		else:
		    f.write(ID_NucleoSeq[i]+'\n')
    	    f.close()
        else:
	    continue

































































































































































































































































































































































































































































    
