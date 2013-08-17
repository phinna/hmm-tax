#!/usr/bin/env python
################################################
# Topic: Split  taxonomy into different levels #
#        and store in several files.           #
#                                              #
################################################

def split_taxonomy_list(OtuFiles,taxonomy_level,output_dir):
    split_taxonomy={7:'k_taxonomy.txt',6:'p_taxonomy.txt',5:'c_taxonomy.txt',
                    4:'o_taxonomy.txt',3:'f_taxonomy.txt',2:'g_taxonomy.txt',
                    1:'s_taxonomy.txt'} 

    for OF in OtuFiles:
        
        f=open(OF,'U')
        
	if taxonomy_level==7:
	    wk=open(output_dir+'/k_taxonomy.txt','a')
        elif taxonomy_level==6:
            wp=open(output_dir+'/p_taxonomy.txt','a')
        elif taxonomy_level==5:
            wc=open(output_dir+'/c_taxonomy.txt','a')
        elif taxonomy_level==4:
	    wo=open(output_dir+'/o_taxonomy.txt','a')
        elif taxonomy_level==3:
	    wf=open(output_dir+'/f_taxonomy.txt','a')
	elif taxonomy_level==2:
	    wg=open(output_dir+'/g_taxonomy.txt','a')
        elif taxonomy_level==1:
	    ws=open(output_dir+'/s_taxonomy.txt','a')
      
	for line in f:
	    taxonomy_list=line.split()
	    if taxonomy_level==7:
 	        k_list=[taxonomy_list[0],'\t',taxonomy_list[1]]
                wk.write(''.join(k_list)+'\n')
            elif taxonomy_level==6:
	    	p_list=[taxonomy_list[0],'\t',taxonomy_list[2]]
  	        wp.write(''.join(p_list)+'\n')
            elif taxonomy_level==5:
                c_list=[taxonomy_list[0],'\t',taxonomy_list[3]]
  	        wc.write(''.join(c_list)+'\n')
            elif taxonomy_level==4:
  	        o_list=[taxonomy_list[0],'\t',taxonomy_list[4]]
	        wo.write(''.join(o_list)+'\n')
            elif taxonomy_level==3:
  	        f_list=[taxonomy_list[0],'\t',taxonomy_list[5]]
	        wf.write(''.join(f_list)+'\n')
            elif taxonomy_level==2:
  	        g_list=[taxonomy_list[0],'\t',taxonomy_list[6]]
	        wg.write(''.join(g_list)+'\n')
            elif taxonomy_level==1:
        	s_list=[taxonomy_list[0],'\t',taxonomy_list[7]]
	        ws.write(''.join(s_list)+'\n')
  	
  
	f.close()
	if taxonomy_level==7:
	    wk.close()
	elif taxonomy_level==6:
	    wp.close()
	elif taxonomy_level==5:
	    wc.close()
	elif taxonomy_level==4:
	    wo.close()
	elif taxonomy_level==3:
	    wf.close()
	elif taxonomy_level==2:
	    wg.close()
        elif taxonomy_level==1:
	    ws.close()
    return split_taxonomy[taxonomy_level]

def main():

    OtuFiles=['61_otu_taxonomy.txt']#,'64_otu_taxonomy.txt','67_otu_taxonomy.txt','70_otu_taxonomy.txt',
          #'73_otu_taxonomy.txt','76_otu_taxonomy.txt','79_otu_taxonomy.txt','82_otu_taxonomy.txt',
          #'85_otu_taxonomy.txt','88_otu_taxonomy.txt','88_otu_taxonomy.txt','91_otu_taxonomy.txt',
          #'94_otu_taxonomy.txt','97_otu_taxonomy.txt','99_otu_taxonomy.txt']
    taxonomy_level=6
    output_dir='IDseq'
    split_taxonomy_list(OtuFiles,taxonomy_level,output_dir)


if __name__=="__main__":
    main()


