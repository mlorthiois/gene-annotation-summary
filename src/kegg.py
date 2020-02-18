import requests
import re


def kegg(ncbi, output_file):
    """Find pathway in the Go database from NCBI Gene ID.

    Find KEGG pathways of a protein (from NCBI Gene ID), 
    and write them in a column of a HTML table.

    Args:
        ncbi (str) : NCBI Gene ID. For example : '5888'.
        output_file (open file) : file to write in.
    """
    print('\tKegg ...')

    r_url = "http://rest.kegg.jp/conv/genes/ncbi-geneid:{}".format(ncbi)
    r = requests.get(r_url)
    if len(r.text) != 1:
        # Extract KEGG ID from request
        kegg_id = r.text.rstrip().split('\t')[1]
        organism_id = kegg_id[:3]
        url = "https://www.genome.jp/dbget-bin/www_bget?{}".format(kegg_id)

        # Write KEGG ID in the HTML table
        output_file.write(f"<td><a href={url}>{kegg_id}</a></td>")

        # Make request and extract KEGG pathways in a list
        r_url = "http://rest.kegg.jp/get/{}".format(kegg_id)
        r = requests.get(r_url)
        pathway_list = re.findall("("+organism_id+"\d+\s{2}.*)", r.text)

        # Write KEGG Pathways in the HTML table
        output_file.write('<td><div class="scroll">')
        if pathway_list != []:
            for path in pathway_list:
                path_id = path.split(' ')[0]
                path_name = path.split('  ')[1]
                link = f"https://www.genome.jp/dbget-bin/www_bget?{path_id}"
                output_file.write(f"<a href={link}>{path_id}</a>: {path_name}<br>")
        else:
            output_file.write('<i>No data found</i>')
        output_file.write('</div></td>')
    else:
        output_file.write('<td><i>No data found</i></td>'*2)
