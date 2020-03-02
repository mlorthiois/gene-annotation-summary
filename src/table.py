import webbrowser
import os


def init_table(output_file):
    """
    Init the table with the opening and reading of the template HTML file
    """
    with open("ressources/head.html", "r") as head_file:
        output_file.write(head_file.read())


def init_row(line, output_file):
    """
    Init the row by reading the query file, extracting, and writing the gene
    symbol and organism in the HTML table.

    Returns :
        gene (str) : The gene symbol alone. For example : 'RAD51'
        organism (str) : The organism alone. For example : 'homo_sapiens'
    """
    colonne = line.split(",")
    gene = colonne[0]
    organism = colonne[1].rstrip('\n')
    print(f"Traitement de {gene} / {organism}")
    writ_org = organism.replace('_', ' ').capitalize()
    output_file.write(f"<tr><td>{gene}<br><i>{writ_org}</i></td>")
    return gene, organism


def end_table(output_file, txt):
    """End the table by :
    - Reading, and writing the end of the template HTML file.
    - Changing the color of the text widget in green.
    - Opening the Results.html in browser
    """
    with open("ressources/end.html", "r") as end_html:
        output_file.write(end_html.read())
    output_file.close()
    txt.configure(foreground='green')
    print('Done')
    webbrowser.open('file://' + os.path.realpath('Results.html'))
