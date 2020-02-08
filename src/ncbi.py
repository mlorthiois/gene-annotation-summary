from Bio import Entrez
import re

gene = 'RAD51'
organism = 'homo_sapiens'


def ncbi_gene_id(gene, organism, output_file):
    print('\tNCBI...')
    Entrez.email = 'matthias.lorthiois@univ-rouen.fr'
    term = "({}[Gene Name]) AND {}[Organism]".format(gene, organism)
    handle = Entrez.esearch(db="Gene", term=term, retmax='20')
    records = Entrez.read(handle)
    output_file.write("<td><div class='scroll'>")
    gene_id = str(records['IdList'][0])
    output_file.write(
        "<a href='https://www.ncbi.nlm.nih.gov/gene/{}'>{}</a>".format(gene_id, gene_id))
    output_file.write("</div></td>")


def ncbi_rna_id(gene, organism, output_file):
    term = "({}[Gene Name]) AND {}[Organism]".format(gene, organism)
    handle = Entrez.esearch(db="nucleotide", term=term)
    records = Entrez.read(handle)
    ID = records['IdList']
    handle = Entrez.efetch(db="nucleotide", id=ID, rettype="acc")
    records = handle.read().split('\n')
    output_file.write("<td><div class='scroll'>")
    printed_count = 0
    for rna_id in records:
        if re.match('.M_', rna_id):
            link = "https://www.ncbi.nlm.nih.gov/nuccore/{}".format(rna_id)
            output_file.write("<a href='{}'>{}</a><br>".format(link, rna_id))
            printed_count += 1
    if printed_count == 0:
        output_file.write('<i>No data found</i>')
    output_file.write("</div></td>")


def ncbi_prot_id(gene, organism, output_file):
    term = "({}[Gene Name]) AND {}[Organism]".format(gene, organism)
    handle = Entrez.esearch(db="protein", term=term)
    records = Entrez.read(handle)
    ID = records['IdList']
    handle = Entrez.efetch(db="protein", id=ID, rettype="acc")
    records = handle.read().split('\n')
    output_file.write("<td><div class='scroll'>")
    printed_count = 0
    for prot_id in records:
        if re.match('.P_', prot_id):
            link = "https://www.ncbi.nlm.nih.gov/protein/{}".format(prot_id)
            output_file.write("<a href='{}'>{}</a><br>".format(link, prot_id))
            printed_count = 1
    if printed_count == 0:
        output_file.write('<i>No data found</i>')
    output_file.write("</div></td>")
