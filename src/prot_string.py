import requests

#Multi requête OK
def string(uniprot_id, output_file):
    print("\tString ...")
    string_id = []
    r_id = "\r".join(uniprot_id)
    url = "https://string-db.org/api/json/get_string_ids?identifiers={}".format(r_id)
    r = requests.get(url)
    if r.ok:
        r = r.json()
        if r != []:
            output_file.write("<td><div class='scroll'>")
            for i in r:
                id = i['stringId']
                if id not in string_id:
                    string_id.append(id)
                    link = "https://string-db.org/api/highres_image/network?identifiers={}".format(id)
                    output_file.write("<a href='{}'>".format(link)+id+"</a><br>")
            output_file.write("</div></td>")
        else:
            output_file.write("<td><i>No data found</i></td>")
    else:
        output_file.write("<td><i>No data found</i></td>")
