from Bio import Entrez
import re
import json


def ncbi_gene_id(gene, organism, output_file):
    """Find NCBI Gene ID from gene symbol and organism.

    Find the Gene ID from NCBI Gene, with BioPython,
    and write it in the HTML table.

    Args:
        gene_symbol (str) : For example : 'RAD51'
        organism (str) : Form example : 'homo_sapiens'
        output_file (open file)

    Returns :
        gene_id (str) : the NCBI Gene ID. For example : '5888'.
    """

    print('\tNCBI...')

    # Request with ESearch
    Entrez.email = 'matthias.lorthiois@univ-rouen.fr'
    term = f"({gene}[Gene Name]) AND {organism}[Organism]"
    handle = Entrez.esearch(db="Gene", term=term, retmax='20')
    records = Entrez.read(handle)
    gene_id = str(records['IdList'][0])

    # Extract the NCBI Gene ID and the Official Gene Name with EFetch
    handle = Entrez.efetch(db="Gene", id=gene_id,
                           rettype="docsum", retmode='json')
    record = json.loads(handle.read())
    temp_id = record['result']['uids'][0]
    official_name = record['result'][temp_id]['description']

    # Write the Official Gene Name in the HTML table
    output_file.write("<td><div class='scroll'>")
    output_file.write(official_name)
    output_file.write("</div></td>")

    # Write the NCBI Gene ID in the HTML table
    output_file.write("<td><div class='scroll'>")
    url = f"https://www.ncbi.nlm.nih.gov/gene/{gene_id}"
    output_file.write(f"<a href='{url}'>{gene_id}</a>")
    output_file.write("</div></td>")

    return gene_id


def ncbi_rna_id(gene, organism, output_file):
    """Find NCBI RefSeq RNA ID from gene symbol and organism.

    Find the Gene RefSeq IDs from the NCBI Gene ID, with BioPython,
    and write them in the HTML table.

    Args:
        gene_symbol (str) : For example : 'RAD51'
        organism (str) : Form example : 'homo_sapiens'
        output_file (open file)
    """

    # Request with ESearch and Extract the RefSeq IDs
    term = f"({gene}[Gene Name]) AND {organism}[Organism]"
    handle = Entrez.esearch(db="nucleotide", term=term)
    records = Entrez.read(handle)
    ID = records['IdList']

    # Request with EFetch the RefSeq RNA IDs
    handle = Entrez.efetch(db="nucleotide", id=ID, rettype="acc")
    records = handle.read().split('\n')
    output_file.write("<td><div class='scroll'>")

    # Write the RefSeq RNA IDs in the HTML table
    printed_count = 0
    for rna_id in records:
        if re.match('.M_', rna_id):  # Write only the conform IDs
            link = f"https://www.ncbi.nlm.nih.gov/nuccore/{rna_id}"
            output_file.write(f"<a href='{link}'>{rna_id}</a><br>")
            printed_count += 1
    if printed_count == 0:  # If no ID written, write No data found
        output_file.write('<i>No data found</i>')
    output_file.write("</div></td>")


def ncbi_prot_id(gene, organism, output_file):
    """Find NCBI RefSeq Proteins ID from gene symbol and organism.

    Find the RefSeq Protein IDs from the NCBI Gene ID, with BioPython,
    and write them in the HTML table.

    Args:
        gene_symbol (str) : For example : 'RAD51'
        organism (str) : Form example : 'homo_sapiens'
        output_file (open file)
    """

    # Request with ESearch and Extract the RefSeq IDs
    term = f"({gene}[Gene Name]) AND {organism}[Organism]"
    handle = Entrez.esearch(db="protein", term=term)
    records = Entrez.read(handle)
    ID = records['IdList']

    # Request with EFetch the RefSeq Protein IDs
    handle = Entrez.efetch(db="protein", id=ID, rettype="acc")
    records = handle.read().split('\n')
    output_file.write("<td><div class='scroll'>")
    printed_count = 0

    # Write the RefSeq Protein IDs in the HTML table
    for prot_id in records:
        if re.match('.P_', prot_id):  # Write only the conforms IDs
            link = f"https://www.ncbi.nlm.nih.gov/protein/{prot_id}"
            output_file.write(f"<a href='{link}'>{prot_id}</a><br>")
            printed_count = 1
    if printed_count == 0:
        output_file.write('<i>No data found</i>')
    output_file.write("</div></td>")
