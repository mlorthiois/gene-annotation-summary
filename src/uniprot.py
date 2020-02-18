import requests


def uniprot(gene, organism, output_file):
    """Search for the UniProtKB ID(s).

    Searching for the ID(s) and the Official Protein Names corresponding to
    the gene symbol and the organism, and writes them in the HTML table.

    Args:
        gene_symbol (str)
        organism (str)
        output_file (open file)

    Return:
        uniprot_id (list) : for example : ['P14713', 'B0FWI9']
    """

    print("\tUniprot ...")

    # Request
    domain = "https://www.uniprot.org/uniprot"
    query = f"?query=gene_exact%3A{gene}+organism%3A{organism}"
    extend = "columns=id,protein_names&format=tab"
    r = requests.get(f"{domain}/{query}&{extend}")
    result = r.text.splitlines()

    # Extract Uniprot IDs and Offical Protein Names
    uniprot_id = []
    uniprot_name = []
    if result != []:
        del(result[0])  # Remove the header
        for line in result:  # Extracting IDs and names
            colonne = line.split('\t')
            id = colonne[0]
            name = colonne[1]
            uniprot_id.append(id)
            if colonne[1] not in uniprot_name:
                uniprot_name.append(name)

        # Write the Uniprot IDs
        output_file.write("<td><div class='scroll'>")
        for id in uniprot_id:
            output_file.write(f'<a href="{domain}/{id}">{id}</a><br>')
        output_file.write("</div></td>")

        # Write the Uniprot Offical Names
        output_file.write("<td><div class='scroll'>")
        output_file.write(f"{'<br>'.join(uniprot_name)}</div></td>")
        return uniprot_id
    else:
        output_file.write("<td><i>No data found</i></td>"*2)
        return uniprot_id
