import webbrowser
import os


def read_file():
    gene_file = open("ressources/GeneSymbols.txt", "r")
    gene_content = gene_file.readlines()
    return gene_content


def init_table(output_file):
    with open("ressources/head.html", "r") as head_file:
        output_file.write(head_file.read())


def init_row(line, output_file):
    colonne = line.split(",")
    gene = colonne[0]
    organism = colonne[1].rstrip('\n')
    print(f"Traitement de {gene} / {organism}")
    output_file.write(f"<tr><td>{gene}</td><td>{organism.replace('_', ' ')}</td>")
    return gene, organism


def end_table(output_file, txt):
    with open("ressources/end.html", "r") as end_html:
        output_file.write(end_html.read())
    output_file.close()
    txt.configure(foreground='green')
    print('Done')
    webbrowser.open('file://' + os.path.realpath('output.html'))
