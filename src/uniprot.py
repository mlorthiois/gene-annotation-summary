import requests
import xml.etree.ElementTree as ET

def uniprot(gene, organism, output_file):
    uniprot_id = []
    uniprot_name=[]
    r = requests.get("https://www.uniprot.org/uniprot/?query=gene_exact%3A{}+organism%3A{}&columns=id,protein_names&format=tab".format(gene,organism))
    #Possible d'ajouter +fragment%3Ano après l'organism et avant le & pour filtrer les fragments
    result=r.text
    result=result.splitlines()
    if result != [] :
        del(result[0])
        for line in result:
            colonne = line.split('\t')
            uniprot_id.append(colonne[0])
            if colonne[1] not in uniprot_name :
                uniprot_name.append(colonne[1])
        output_file.write("<td><div class='scroll'>"+"<br>".join(uniprot_id)+"</div></td>")
        output_file.write("<td><div class='scroll'>"+"<br>".join(uniprot_name)+"</div></td>")
        return uniprot_id
    else:
        output_file.write("<td><i>No data found</i></td>"*2)
        return uniprot_id

def string(uniprot_id, output_file):
    for id in uniprot_id:
        url="https://string-db.org/api/json/get_string_ids?identifiers={}".format(id)
        r = requests.get(url)
        if r.ok:
            r=r.json()
            if len(r)!=0 and r!= []:
                output_file.write("<td><div class='scroll'>"+r[0]['stringId']+"</div></td>")
                return
    output_file.write("<td><i>No data found</i></td>")

def pdb(uniprot_id, output_file):
    output_file.write("<td><div class='scroll'>")
    pdb_id=[]
    url = "https://www.rcsb.org/pdb/rest/search"
    for id in uniprot_id:
        query= "<orgPdbQuery><queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType><accessionIdList>{}</accessionIdList></orgPdbQuery>".format(id)
        header={"Content-Type":"Application/x-www-form-urlencoded"}
        r = requests.post(url,data=query,headers=header)
        if r.text != "null\n":
            r = r.text.splitlines()
            for line in r:
                colonne = line.split(':')
                if colonne[0] not in pdb_id:
                    pdb_id.append(colonne[0])
    if pdb_id != []:
        for pdb_access in pdb_id:
            r = requests.get("http://www.rcsb.org/pdb/rest/customReport.xml?pdbids={}&customReportColumns=structureTitle,&format=xml".format(pdb_access))
            xml = ET.fromstring(r.text)
            output_file.write(pdb_access + " : " + xml[0][1].text + "<br>")
    else:
        output_file.write("<i>No data found</i>")
    output_file.write("</div></td>")
