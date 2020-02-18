import requests


def string(uniprot_id, output_file):
    """Find protein network in the Prosite database from UniprotKB ID.

    Find Protein network (from UniprotKB ID),
    and write their ID in a column of a HTML table.

    Args:
        uniprot_id (list)
        output_file (open file)
    """
    print("\tString ...")
    string_id = []
    r_id = "\r".join(uniprot_id)  # Single request with all uniprot IDs
    domain = "https://string-db.org/api"
    url = f"{domain}/json/get_string_ids?identifiers={r_id}"
    r = requests.get(url)
    if r.ok:
        r = r.json()
        if r != []:
            output_file.write("<td><div class='scroll'>")
            for i in r:
                # Extract String ID and write it if not already written
                id = i['stringId']
                if id not in string_id:
                    string_id.append(id)
                    link = f"{domain}/highres_image/network?identifiers={id}"
                    output_file.write(f"<a href='{link}'>{id}</a><br>")
            output_file.write("</div></td>")
        else:
            output_file.write("<td><i>No data found</i></td>")
    else:
        output_file.write("<td><i>No data found</i></td>")
