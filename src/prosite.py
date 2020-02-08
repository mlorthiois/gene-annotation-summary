import requests

# Revu ok multirecherche


def prosite(uniprot_id, output_file):
    print("\tProsite ...")
    output_file.write("<td><div class='scroll'>")
    prosite_id = []
    r_id = "%0A".join(uniprot_id[:1])
    url = 'https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}&output=json'.format(
        r_id)
    r = requests.get(url).json()
    for i in r['matchset']:
        if i['signature_ac'] not in prosite_id:
            prosite_id.append(i['signature_ac'])
    if prosite_id != []:
        for id in prosite_id:
            url = "https://prosite.expasy.org/cgi-bin/prosite/nicedoc.pl?{}".format(
                id)
            output_file.write("<a href="+url+">{}</a><br>".format(id))
            url = "https://prosite.expasy.org/cgi-bin/prosite/PSView.cgi?ac={}&onebyarch=1&hscale=0.6".format(
                id)
            output_file.write(
                "<a href="+url+">Graphical view</a><br><br>".format(id))
    else:
        output_file.write("<i>No data found</i>")
    output_file.write("</div></td>")
