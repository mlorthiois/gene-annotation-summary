import requests
import xml.etree.ElementTree as ET


def pdb(uniprot_id, output_file):
    print("\tPDB ...")
    output_file.write("<td><div class='scroll'>")
    pdb_id = []
    url = "https://www.rcsb.org/pdb/rest/search"
    for id in uniprot_id:
        query = "<orgPdbQuery><queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType><accessionIdList>{}</accessionIdList></orgPdbQuery>".format(
            id)
        header = {"Content-Type": "Application/x-www-form-urlencoded"}
        r = requests.post(url, data=query, headers=header)
        if r.text != "null\n":
            r = r.text.splitlines()
            for line in r:
                colonne = line.split(':')
                if colonne[0] not in pdb_id:
                    pdb_id.append(colonne[0])
    if pdb_id != []:
        for pdb_access in pdb_id:
            r = requests.get(
                "http://www.rcsb.org/pdb/rest/customReport.xml?pdbids={}&customReportColumns=structureTitle,&format=xml".format(pdb_access))
            xml = ET.fromstring(r.text)
            link = "<a href='https://www.rcsb.org/structure/{}'>{}</a>".format(pdb_access, pdb_access)
            output_file.write(link + " : " + xml[0][1].text + "<br>")
    else:
        output_file.write("<i>No data found</i>")
    output_file.write("</div></td>")
