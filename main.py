#! /usr/src/env python
from src.ensembl import *
from src.table import *
from src.uniprot import *

output_file=open("output.html","w")
gene_file=read_file()

init_table(output_file)
for line in gene_file:
    gene, organism = init_row(line, output_file)
    #############################################################################################Ensembl
    ens_url=ensembl_db(organism)
    if ens_url!="0": #Evite de se connecter si pas trouvé dans la base de données
        ens_ID=ensembl_id(gene, organism, output_file, ens_url)
        ensembl_trans_prot(ens_ID, output_file, ens_url, organism)
        ens_orthologs(ens_ID,organism,ens_url,output_file)
    else:
        output_file.write("<td><i>No data found</i></td>"*4)
    #############################################################################################Uniprot
    uniprot_id=uniprot(gene, organism, output_file)
    if uniprot_id != []:#############################################################################################String
        string(uniprot_id, output_file)
    #############################################################################################PDB
        pdb(uniprot_id, output_file)
    else:
        output_file.write("<td><i>No data found</i></td>"*2)
    #############################################################################################End
    output_file.write("</tr>")
end_table(output_file)