import requests


def prosite(uniprot_id, output_file):
    """Find protein motifs in the Prosite database from UniprotKB ID.

    Find Protein motifs (from UniprotKB ID),
    and write their ID and graphical view in a column of a HTML table.

    Args:
        uniprot_id (list)
        output_file (open file)
    """
    print("\tProsite ...")

    # Request
    r_id = uniprot_id[0]
    domain = "https://prosite.expasy.org/cgi-bin/prosite"
    url = f'{domain}/PSScan.cgi?seq={r_id}&output=json'
    r = requests.get(url).json()

    # Extract ID and find if it's a pattern/profile (import for graphical view)
    prosite_id = {}
    for i in r['matchset']:
        acc_id = i['signature_ac']
        if 'level_tag' in i:  # level_tag in matchset if id = pattern
            prosite_id[acc_id] = 'pattern'
        else:
            prosite_id[acc_id] = 'profile'

    # Write ID and additional graphical view link if it's a profile
    output_file.write("<td><div class='scroll'>")
    if prosite_id != {}:
        for id in prosite_id:
            url = f"{domain}/nicedoc.pl?{id}"
            output_file.write(f'<a href="{url}">{id}</a>')

            if prosite_id[id] == 'profile':  # If profile: add graphical view
                url = f"{domain}/PSView.cgi?ac={id}"
                link = f": <a href='{url}'>Graphical view</a>"
                output_file.write(link)
            output_file.write("<br>")
    else:
        output_file.write("<i>No data found</i>")
    output_file.write("</div></td>")
