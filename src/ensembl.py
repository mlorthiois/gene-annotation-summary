import requests


def ens_db(organism):
    """Choose the right domain.

    Extract, with a request based on the organism, the right url to use.

    Args:
        organism (str)

    Returns:
        url (url) : The right url domain in str format. For example:

        'plants.ensembl.org'

        If the organism is not identified in the db, returns '0'
    """

    print("\tEnsembl ...")
    dic = {
        'EnsemblBacteria': 'bacteria.ensembl.org',
        "EnsemblFungi": 'fungi.ensembl.org',
        'EnsemblVertebrates': 'ensembl.org',
        'EnsemblPlants': 'plants.ensembl.org'
        }

    server = "https://rest.ensembl.org"
    ext = f"/info/genomes/{organism}?"
    headers = {"Content-Type": "application/json"}
    r = requests.get(server+ext, headers=headers)

    if not r.ok:  # If species not found
        ens_url = "0"
    else:
        decoded = r.json()
        if decoded["division"] in dic:  # Extract domain from request
            ens_url = dic[decoded['division']]  # Extract domain from dic
        else:
            ens_url = "0"
    return ens_url


def ens_id(gene, organism, output_file, ens_url):
    """Search for the Ensemble Gene ID(s).

    Searching for the ID(s) corresponding to the gene symbol and the species,
    and writes them in the HTML table.

    Args:
        gene_symbol (str)
        organism (str)
        output_file (open file)
        ens_url (str) : ensembl domain corresponding to the organism

    Return:
        gene_id (list) : for example : ['AT2G18790', 'ENSG00000051180']
    """

    if ens_url == "0":  # If organism not found, break the function
        output_file.write("<td><i>No data found</i></td>")
        return

    server = "https://rest.ensembl.org"
    ext = f"/xrefs/symbol/{organism}/{gene}?"
    headers = {"Content-Type": "application/json"}
    r = requests.get(server+ext, headers=headers)
    decoded = r.json()

    if r.ok and len(decoded) != 0:
        ens_ID = []
        for i in range(len(decoded)):  # Browser all the ID if multiple
            ID = decoded[i]["id"]
            ens_ID.append(ID)

        output_file.write('<td><div class="scroll">')
        for ID in ens_ID:  # Write in HTML table the linkable ID
            url = f"https://{ens_url}/{organism}/Gene/Summary?g={ID}"
            output_file.write(f"<a href={url}>{ID}</a><br>")

            url = f"https://{ens_url}/{organism}/Location/View?db=core;g={ID}"
            output_file.write(f"<a href={url}>View in Ensembl Browser</a><br>")

            if len(ens_ID) > 1:  # If more than 1 ID to show, add line break
                output_file.write("<br>")
        output_file.write('</div></td>')
    else:
        ens_ID = ["Not found"]
        output_file.write("<td><i>No data found</i></td>")
    return ens_ID


def ens_rna_prot(ens_ID, output_file, ens_url, organism):
    """Search for the Ensemble Transcript and Protein ID(s).

    Searching for the ID(s) corresponding to the ensembl ID,
    and writes them in 2 columns of the HTML table.

    Args:
        ensembl_id (list) : for example: ['AT2G18790', 'ENSG00000051180']
        output_file (open file)
        ens_url (str) : ensembl domain corresponding to the organism
        organism (str) : needed to construct the url
    """

    if ens_url == "0":  # If organism not found, break the function
        output_file.write("<td><i>No data found</i></td>"*2)
        return

    dic = {}  # Data structure to store the different ensembl gene IDs
    server = "https://rest.ensembl.org"

    # Search for the transcript and protein ensembl IDs from the gene ID
    for ID in ens_ID:
        dic[ID] = {}
        ext = f"/lookup/id/{ID}?expand=1"
        r = requests.get(
            server+ext, headers={"Content-Type": "application/json"})
        if r.ok:
            decoded = r.json()
            # store for each geneid the trans IDs (key) and prot IDs (value)
            for i in decoded["Transcript"]:
                dic[ID][i["id"]] = "Empty"  # Init the dic to an empty value
                try:
                    dic[ID][i["id"]] = i["Translation"]["id"]
                except:
                    pass
        else:
            output_file.write(
                '<td><i>No data found</i></td>'*2)
            return

    # Write the transcript IDs in the HTML table
    output_file.write('<td><div class="scroll">')
    for ID in ens_ID:
        for transcript in dic[ID]:
            if transcript != "Not found":
                var = "Transcript/Summary?t"
                url = f"https://{ens_url}/{organism}/{var}={transcript}"
                output_file.write(f"<a href={url}>{transcript}</a><br>")
    output_file.write('</div></td>')

    # Write the protein IDs in the HTML table
    output_file.write('<td><div class="scroll">')
    for ID in ens_ID:
        for transcript in dic[ID]:
            protein = dic[ID][transcript]
            if protein != "Empty" and protein != "Not found":
                var = "Transcript/ProteinSummary?g"
                url = f"https://{ens_url}/{organism}/{var}={ID};t={transcript}"
                output_file.write(f"<a href={url}>{protein}<br></a>")
    output_file.write('</div></td>')


def ens_orthologs(ens_ID, organism, ens_url, output_file):
    """Search for the Ensemble Ortholog Gene list.

    Searching, from Ensembl Gene ID(s), the corresponding Ortholog Gene list,
    and writes it in a column of the HTML table.

    Args:
        ensembl_id (list) : for example: ['AT2G18790', 'ENSG00000051180']
        organism (str) : needed to construct the url
        ens_url (str) : ensembl domain corresponding to the organism
        output_file (open file)
    """
    if ens_url == "0":  # If organism not found, break the function
        output_file.write("<td><i>No data found</i></td>")
        return

    # Write Ortholog links from IDs in the HTML table
    output_file.write('<td><div class="scroll">')
    for ID in ens_ID:
        if ens_ID != ["Not found"]:
            var = "Gene/Compara_Ortholog?db=core;g"
            url = f"https://{ens_url}/{organism}/{var}={ID}"
            output_file.write(f"<a href={url}>Orthologs list</a><br>")
        else:
            output_file.write('<i>No data found</i>')
        if len(ens_ID) > 1:  # If multiple link to write, add line break
            output_file.write("<br>")
    output_file.write('</div></td>')
