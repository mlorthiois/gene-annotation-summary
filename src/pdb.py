import requests
import xml.etree.ElementTree as ET


def pdb(uniprot_id, output_file):
    """Find structure in the Protein Database Data Bank from UniprotKB ID.

    Find Protein Structure (from UniprotKB ID),
    and write their ID and label in a column of a HTML table.

    Args:
        uniprot_id (list)
        output_file (open file)
    """
    print("\tPDB ...")

    pdb_id = []
    url = "https://www.rcsb.org/pdb/rest/search"

    # Request
    for id in uniprot_id:
        query = f"<orgPdbQuery><queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType><accessionIdList>{id}</accessionIdList></orgPdbQuery>"
        header = {"Content-Type": "Application/x-www-form-urlencoded"}
        r = requests.post(url, data=query, headers=header)

        # Extract PDB ID
        if r.text != "null\n":
            r = r.text.splitlines()
            for line in r:
                colonne = line.split(':')
                if colonne[0] not in pdb_id:
                    pdb_id.append(colonne[0])

    # Request Structure label and write in HTML table
    output_file.write("<td><div class='scroll'>")
    if pdb_id != []:
        for pdb_access in pdb_id:
            # Request structure label
            domain = "http://www.rcsb.org/pdb/rest/customReport.xml?"
            extend = "customReportColumns=structureTitle,&format=xml"
            r = requests.get(f"{domain}pdbids={pdb_access}&{extend}")
            xml = ET.fromstring(r.text)
            pathway = xml[0][1].text

            # Write in HTML table
            url = f"https://www.rcsb.org/structure/{pdb_access}"
            link = f"<a href='{url}'>{pdb_access}</a>"
            output_file.write(f"{link}: {pathway}<br>")
    else:
        output_file.write("<i>No data found</i>")
    output_file.write("</div></td>")
