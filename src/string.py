import requests

def string(uniprot_id, output_file):
    print("\tString ...")
    for id in uniprot_id:
        url="https://string-db.org/api/json/get_string_ids?identifiers={}".format(id)
        r = requests.get(url)
        if r.ok:
            r=r.json()
            if len(r)!=0 and r!= []:
                output_file.write("<td><div class='scroll'><a href='https://string-db.org/api/highres_image/network?identifiers={}'>".format(id)+r[0]['stringId']+"</a></div></td>")
                return
    output_file.write("<td><i>No data found</i></td>")