import requests

############################################################################################
def ensembl_db(organism):
    print("\tEnsembl ...")
    dic = { 'EnsemblBacteria':'bacteria.ensembl.org',"EnsemblFungi":'fungi.ensembl.org',"EnsemblBacteria":'bacteria.ensembl.org',
            'EnsemblVertebrates':'ensembl.org','EnsemblPlants':'plants.ensembl.org'}
    server = "https://rest.ensembl.org"
    ext = "/info/genomes/{}?".format(organism)
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    if not r.ok:
        ens_url="0"
    else:
        decoded = r.json()
        if decoded["division"] in dic:
            ens_url = dic[decoded['division']]
        else:
            ens_url = "0"
    return ens_url
############################################################################################
def ensembl_id(gene, organism, output_file, ens_url):
    server="https://rest.ensembl.org"
    ext = "/xrefs/symbol/{}/{}?".format(organism,gene)
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    decoded = r.json()
    if r.ok and len(decoded)!= 0:
        ens_ID=[]
        for i in range(len(decoded)):
            ID=decoded[i]["id"]
            ens_ID.append(ID)
    else:
        ens_ID=["Not found"]
    if ens_ID!=["Not found"]:
        output_file.write('<td><div class="scroll">')
        for ID in ens_ID:
            url="https://{}/{}/Gene/Summary?g={}".format(ens_url,organism,ID)
            output_file.write("<a href={}>{}</a><br>".format(url,ID))
            url="https://{}/{}/Location/View?db=core;g={}".format(ens_url,organism,ID)
            output_file.write("<a href={}>View in Ensembl Browser</a><br>".format(url))
            if len(ens_ID)>1:
                output_file.write("<br>")
        output_file.write('</div></td>')
    else:
        output_file.write("<td><i>No data found</i></td>")
    return ens_ID
############################################################################################
def ensembl_trans_prot(ens_ID, output_file, ens_url, organism):
    output_file.write('<td><div class="scroll">')
    dic={}
    server= "https://rest.ensembl.org"
    for ID in ens_ID: #Parfois lusieurs ID par Gene
        dic[ID]={}
        ext = "/lookup/id/{}?expand=1".format(ID)
        r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
        if r.ok:
            decoded = r.json()
            for i in decoded["Transcript"]:
                dic[ID][i["id"]]="Empty"
                try:
                    dic[ID][i["id"]]=i["Translation"]["id"]
                except:
                    pass
        else:
            output_file.write('<i>No data found</i></td><td><i>No data found</i>')
            return
    for ID in ens_ID: #Affiche les transcrits et protéines pour tous les ID du gène   
        for transcript in dic[ID]:
            if transcript!="Not found":
                url="https://{}/{}/Transcript/Summary?t={}".format(ens_url,organism,transcript)
                output_file.write("<a href={}>{}</a><br>".format(url,transcript))
    output_file.write('</div></td>')
    output_file.write('<td><div class="scroll">')
    for ID in ens_ID:
        for transcript in dic[ID]:
            protein=dic[ID][transcript]
            if protein!="Empty" and protein!="Not found":
                url="https://{}/{}/Transcript/ProteinSummary?g={};t={}".format(ens_url,organism,ID,transcript)
                output_file.write("<a href={}>{}<br></a>".format(url,protein))
    output_file.write('</div></td>')
############################################################################################
def ens_orthologs(ens_ID,organism,ens_url,output_file):
    output_file.write('<td><div class="scroll">')   
    for ID in ens_ID:
        if ens_ID!=["Not found"]:
            url="https://{}/{}/Gene/Compara_Ortholog?db=core;g={}".format(ens_url,organism,ID)
            output_file.write("<a href={}>Orthologs list</a><br>".format(url))
        else:
            output_file.write('<i>No data found</i>')
        if len(ens_ID)>1:
            output_file.write("<br>")
    output_file.write('</div></td>')
############################################################################################