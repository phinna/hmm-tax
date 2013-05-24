################################################
# Topic: Classify taxonomy into several groups #
#        and store in several files.           #
#                                              #
################################################
def seperate_taxonomy_list(OtuFiles):
    for OF in OtuFiles:
        FilePath='./gg_12_10_otus/taxonomy/'
        f=open(FilePath+OF,'r')
	wk=open('k_taxonomy.txt','a')
        wp=open('p_taxonomy.txt','a')
	wc=open('c_taxonomy.txt','a')
	wo=open('o_taxonomy.txt','a')
	wf=open('f_taxonomy.txt','a')
	wg=open('g_taxonomy.txt','a')
	ws=open('s_taxonomy.txt','a')
      
	for line in f:
	    
  	    taxonomy_list=line.split()
  	    k_list=[taxonomy_list[0],'\t',taxonomy_list[1]]
  	    p_list=[taxonomy_list[0],'\t',taxonomy_list[2]]
            c_list=[taxonomy_list[0],'\t',taxonomy_list[3]]
  	    o_list=[taxonomy_list[0],'\t',taxonomy_list[4]]
  	    f_list=[taxonomy_list[0],'\t',taxonomy_list[5]]
  	    g_list=[taxonomy_list[0],'\t',taxonomy_list[6]]
  	    s_list=[taxonomy_list[0],'\t',taxonomy_list[7]]
  	
            wk.write(''.join(k_list)+'\n')
  	    wp.write(''.join(p_list)+'\n')
  	    wc.write(''.join(c_list)+'\n')
	    wo.write(''.join(o_list)+'\n')
	    wf.write(''.join(f_list)+'\n')
	    wg.write(''.join(g_list)+'\n')
	    ws.write(''.join(s_list)+'\n')
  
	f.close()
	wk.close()
	wp.close()
	wc.close()
	wo.close()
	wf.close()
	wg.close()
	ws.close()

OtuFiles=['61_otu_taxonomy.txt','64_otu_taxonomy.txt','67_otu_taxonomy.txt','70_otu_taxonomy.txt',
          '73_otu_taxonomy.txt','76_otu_taxonomy.txt','79_otu_taxonomy.txt','82_otu_taxonomy.txt',
          '85_otu_taxonomy.txt','88_otu_taxonomy.txt','88_otu_taxonomy.txt','91_otu_taxonomy.txt',
          '94_otu_taxonomy.txt','97_otu_taxonomy.txt','99_otu_taxonomy.txt']

seperate_taxonomy_list(OtuFiles)


