import requests


def ens_db(organism):
    print("\tEnsembl ...")
    dic = {
        'EnsemblBacteria': 'bacteria.ensembl.org', 
        "EnsemblFungi": 'fungi.ensembl.org', 
        "EnsemblBacteria": 'bacteria.ensembl.org',
        'EnsemblVertebrates': 'ensembl.org', 
        'EnsemblPlants': 'plants.ensembl.org'
        }

    server = "https://rest.ensembl.org"
    ext = f"/info/genomes/{organism}?"
    r = requests.get(server+ext, headers={"Content-Type": "application/json"})
    if not r.ok:
        ens_url = "0"
    else:
        decoded = r.json()
        if decoded["division"] in dic:
            ens_url = dic[decoded['division']]
        else:
            ens_url = "0"
    return ens_url


def ens_id(gene, organism, output_file, ens_url):
    server = "https://rest.ensembl.org"
    ext = f"/xrefs/symbol/{organism}/{gene}?"
    r = requests.get(server+ext, headers={"Content-Type": "application/json"})
    decoded = r.json()
    if r.ok and len(decoded) != 0:
        ens_ID = []
        for i in range(len(decoded)):
            ID = decoded[i]["id"]
            ens_ID.append(ID)
        output_file.write('<td><div class="scroll">')
        for ID in ens_ID:
            url = f"https://{ens_url}/{organism}/Gene/Summary?g={ID}"
            output_file.write(f"<a href={url}>{ID}</a><br>")
            url = f"https://{ens_url}/{organism}/Location/View?db=core;g={ID}"
            output_file.write(
                f"<a href={url}>View in Ensembl Browser</a><br>")
            if len(ens_ID) > 1:
                output_file.write("<br>")
        output_file.write('</div></td>')
    else:
        ens_ID = ["Not found"]
        output_file.write("<td><i>No data found</i></td>")
    return ens_ID


def ens_rna_prot(ens_ID, output_file, ens_url, organism):
    output_file.write('<td><div class="scroll">')
    dic = {}
    server = "https://rest.ensembl.org"
    for ID in ens_ID:  # Parfois lusieurs ID par Gene
        dic[ID] = {}
        ext = f"/lookup/id/{ID}?expand=1"
        r = requests.get(
            server+ext, headers={"Content-Type": "application/json"})
        if r.ok:
            decoded = r.json()
            for i in decoded["Transcript"]:
                dic[ID][i["id"]] = "Empty"
                try:
                    dic[ID][i["id"]] = i["Translation"]["id"]
                except:
                    pass
        else:
            output_file.write(
                '<i>No data found</i></td><td><i>No data found</i>')
            return
    # Write Ens_Transcript_ID
    for ID in ens_ID:
        for transcript in dic[ID]:
            if transcript != "Not found":
                url = f"https://{ens_url}/{organism}/Transcript/Summary?t={transcript}"
                output_file.write(f"<a href={url}>{transcript}</a><br>")
    output_file.write('</div></td>')

    #Print Ens_Prot_ID
    output_file.write('<td><div class="scroll">')
    for ID in ens_ID:
        for transcript in dic[ID]:
            protein = dic[ID][transcript]
            if protein != "Empty" and protein != "Not found":
                url = f"https://{ens_url}/{organism}/Transcript/ProteinSummary?g={ID};t={transcript}"
                output_file.write(f"<a href={url}>{protein}<br></a>")
    output_file.write('</div></td>')


def ens_orthologs(ens_ID, organism, ens_url, output_file):
    output_file.write('<td><div class="scroll">')
    for ID in ens_ID:
        if ens_ID != ["Not found"]:
            url = f"https://{ens_url}/{organism}/Gene/Compara_Ortholog?db=core;g={ID}"
            output_file.write(f"<a href={url}>Orthologs list</a><br>")
        else:
            output_file.write('<i>No data found</i>')
        if len(ens_ID) > 1:
            output_file.write("<br>")
    output_file.write('</div></td>')
