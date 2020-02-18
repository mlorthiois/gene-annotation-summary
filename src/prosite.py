import requests


def prosite(uniprot_id, output_file):
    print("\tProsite ...")
    output_file.write("<td><div class='scroll'>")
    prosite_id = {}
    r_id = uniprot_id[0]
    url = 'https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}&output=json'.format(
        r_id)
    r = requests.get(url).json()
    for i in r['matchset']:
        acc_id = i['signature_ac']
        if 'level_tag' in i:
            prosite_id[acc_id] = 'pattern'
        else :
            prosite_id[acc_id] = 'profile'
    if prosite_id != {}:
        for id in prosite_id:
            url = "https://prosite.expasy.org/cgi-bin/prosite/nicedoc.pl?{}".format(
                id)
            output_file.write("<a href="+url+">{}</a>".format(id))
            
            if prosite_id[id] == 'profile': #if id is a profile and not a pattern : show the graphical view link
                url = "https://prosite.expasy.org/cgi-bin/prosite/PSView.cgi?ac={}&onebyarch=1&hscale=0.6".format(
                id)
                output_file.write(
                    " : <a href="+url+">Graphical view</a>".format(id))
            
            output_file.write("<br>")
            
    else:
        output_file.write("<i>No data found</i>")
    output_file.write("</div></td>")
