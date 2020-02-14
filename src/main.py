#! /usr/bin/env python
from src.ensembl import ens_db, ens_id, ens_rna_prot, ens_orthologs
from src.table import init_table, init_row, end_table
from src.uniprot import uniprot
from src.prosite import prosite
from src.pdb import pdb
from src.pfam import pfam
from src.prot_string import string
from src.ncbi import ncbi_gene_id, ncbi_rna_id, ncbi_prot_id
from src.kegg import kegg
from src.go import go


def txt_done(txt, line_number):
    if line_number > 1:
        cursor = f"{line_number-1}.end"
        txt.tag_config("Finish", foreground="green")
        txt.insert(cursor, " Done", ('Finish'))
        txt.update()


def txt_statut(txt, line_number, step):
    cursor = f"{line_number}.end"
    txt.tag_config("Current", foreground="#E95420")
    txt.insert(cursor, step, ('Current'))
    txt.update()
    txt.delete(f"{'Current'}.first", f"{'Current'}.last")


def main(filename, txt):
    line_number = 1
    output_file = open("Results.html", "w")
    with open(filename, 'r') as gene_file:
        gene_content = gene_file.readlines()
    init_table(output_file)
    for line in gene_content:
        txt_done(txt, line_number)
        gene, organism = init_row(line, output_file)
        # NCBI
        txt_statut(txt, line_number, ' NCBI...',)
        ncbi_main_id = ncbi_gene_id(gene, organism, output_file)
        ncbi_rna_id(gene, organism, output_file)
        ncbi_prot_id(gene, organism, output_file)
        # Ensembl
        txt_statut(txt, line_number, ' EnsEMBL...',)
        ens_url = ens_db(organism)
        ens_ID = ens_id(gene, organism, output_file, ens_url)
        ens_rna_prot(ens_ID, output_file, ens_url, organism)
        ens_orthologs(ens_ID, organism, ens_url, output_file)
        # Proteins
        txt_statut(txt, line_number, ' UniProt...',)
        uniprot_id = uniprot(gene, organism, output_file)

        txt_statut(txt, line_number, ' String...',)
        string(uniprot_id, output_file)

        txt_statut(txt, line_number, ' Protein Data Bank...',)
        pdb(uniprot_id, output_file)

        txt_statut(txt, line_number, ' Pfam...',)
        pfam(uniprot_id, output_file)

        txt_statut(txt, line_number, ' Prosite...',)
        prosite(uniprot_id, output_file)

        txt_statut(txt, line_number, ' KEGG...',)
        kegg(ncbi_main_id, output_file)

        txt_statut(txt, line_number, ' GO...',)
        go(uniprot_id, output_file)
        # End
        output_file.write("</tr>")
        line_number += 1
    
    end_table(output_file, txt)
