from Bio import Entrez
import re
import json


def ncbi_gene_id(gene, organism, output_file):
    print('\tNCBI...')
    Entrez.email = 'matthias.lorthiois@univ-rouen.fr'
    term = f"({gene}[Gene Name]) AND {organism}[Organism]"
    handle = Entrez.esearch(db="Gene", term=term, retmax='20')
    records = Entrez.read(handle)
    gene_id = str(records['IdList'][0])

    handle = Entrez.efetch(db="Gene", id=gene_id, rettype="docsum", retmode='json')
    record = json.loads(handle.read())
    temp_id=record['result']['uids'][0]
    official_name = record['result'][temp_id]['description']

    output_file.write("<td><div class='scroll'>")
    output_file.write(official_name)
    output_file.write("</div></td>")

    output_file.write("<td><div class='scroll'>")
    output_file.write(
        f"<a href='https://www.ncbi.nlm.nih.gov/gene/{gene_id}'>{gene_id}</a>")
    output_file.write("</div></td>")
    return gene_id


def ncbi_rna_id(gene, organism, output_file):
    term = f"({gene}[Gene Name]) AND {organism}[Organism]"
    handle = Entrez.esearch(db="nucleotide", term=term)
    records = Entrez.read(handle)
    ID = records['IdList']

    handle = Entrez.efetch(db="nucleotide", id=ID, rettype="acc")
    records = handle.read().split('\n')
    output_file.write("<td><div class='scroll'>")

    printed_count = 0
    for rna_id in records:
        if re.match('.M_', rna_id):
            link = f"https://www.ncbi.nlm.nih.gov/nuccore/{rna_id}"
            output_file.write(f"<a href='{link}'>{rna_id}</a><br>")
            printed_count += 1
    if printed_count == 0:
        output_file.write('<i>No data found</i>')
    output_file.write("</div></td>")


def ncbi_prot_id(gene, organism, output_file):
    term = f"({gene}[Gene Name]) AND {organism}[Organism]"
    handle = Entrez.esearch(db="protein", term=term)
    records = Entrez.read(handle)
    ID = records['IdList']

    handle = Entrez.efetch(db="protein", id=ID, rettype="acc")
    records = handle.read().split('\n')
    output_file.write("<td><div class='scroll'>")
    printed_count = 0

    for prot_id in records:
        if re.match('.P_', prot_id):
            link = f"https://www.ncbi.nlm.nih.gov/protein/{prot_id}"
            output_file.write(f"<a href='{link}'>{prot_id}</a><br>")
            printed_count = 1
    if printed_count == 0:
        output_file.write('<i>No data found</i>')
    output_file.write("</div></td>")
