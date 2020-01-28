import requests

def uniprot(gene, organism, output_file):
    print("\tUniprot ...")
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
        output_file.write("<td><div class='scroll'>")
        for id in uniprot_id:
            output_file.write('<a href="https://www.uniprot.org/uniprot/{}">{}</a><br>'.format(id, id))
        output_file.write("</td><td><div class='scroll'>"+"<br>".join(uniprot_name)+"</div></td>")
        return uniprot_id
    else:
        output_file.write("<td><i>No data found</i></td>"*2)
        return uniprot_id