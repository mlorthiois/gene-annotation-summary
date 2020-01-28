#! /usr/bin/env python
from src.ensembl import *
from src.table import *
from src.uniprot import *
from src.pfam import *
from src.prosite import *
from src.pdb import *
from src.pfam import *
from src.string import *

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
    #############################################################################################Proteins
    uniprot_id=uniprot(gene, organism, output_file)
    string(uniprot_id, output_file)
    pdb(uniprot_id, output_file)
    pfam(uniprot_id, output_file)
    prosite(uniprot_id,output_file)
    #############################################################################################End
    output_file.write("</tr>")
end_table(output_file)