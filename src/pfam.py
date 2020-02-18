import requests
import xml.etree.ElementTree as ET


def pfam(uniprot_id, output_file):
    pfam_id = []
    print("\tPfam ...")
    output_file.write('<td><div class="scroll">')
    for ID in uniprot_id:
        r = requests.get(
            "http://pfam.xfam.org/protein/{}?output=xml".format(ID))
        xml = ET.fromstring(r.content)
        for match in xml.iter('{https://pfam.xfam.org/}match'):
            if match.attrib['accession'] not in pfam_id:
                pfam_id.append(match.attrib['accession'])
    for ID in pfam_id:
        link = f"https://pfam.xfam.org/family/{ID}"
        output_file.write(f'<a href="{link}">{ID}</a> : <a href="{link}#tabview=tab1">Graphical view</a><br>')
    output_file.write("</div></td>")
