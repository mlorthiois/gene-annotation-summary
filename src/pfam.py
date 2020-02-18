import requests
import xml.etree.ElementTree as ET


def pfam(uniprot_id, output_file):
    """Find protein domains in the Pfam database from UniprotKB ID.

    Find Protein domains (from UniprotKB ID),
    and write their ID and graphical view in a column of a HTML table.

    Args:
        uniprot_id (list)
        output_file (open file)
    """
    print("\tPfam ...")

    # Request Uniprot ID and store domains in pfam_id
    pfam_id = []
    for ID in uniprot_id:
        r = requests.get(
            "http://pfam.xfam.org/protein/{}?output=xml".format(ID))
        xml = ET.fromstring(r.content)
        for match in xml.iter('{https://pfam.xfam.org/}match'):
            if match.attrib['accession'] not in pfam_id:
                pfam_id.append(match.attrib['accession'])

    # Write Pfam IDs and Graphical view in HTML table
    output_file.write('<td><div class="scroll">')
    for ID in pfam_id:
        link = f"<a href='https://pfam.xfam.org/family/{ID}'>{ID}</a>"
        g_url = f"https://pfam.xfam.org/family/{ID}#tabview=tab1"
        g_link = f"<a href='{g_url}'>Graphical view</a>"
        output_file.write(f'{link}: {g_link}<br>')
    output_file.write("</div></td>")
