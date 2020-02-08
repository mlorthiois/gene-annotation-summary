import requests
import re
path_id = {}


def kegg_id():
    print('\tKegg ...')

    ncbi = '5888'
    r_url = "http://rest.kegg.jp/conv/genes/ncbi-geneid:{}".format(ncbi)
    r = requests.get(r_url)
    kegg_id = r.text.rstrip().split('\t')[1]
    url = "https://www.genome.jp/dbget-bin/www_bget?{}".format(kegg_id)
    print("<td><a href={}>{}</a></td>".format(url, kegg_id))

    r_url = "http://rest.kegg.jp/get/{}".format(kegg_id)
    r = requests.get(r_url)
    path_list = re.findall("(hsa\d+\s{2}.*)", r.text)
    for path in path_list:
        path_id[path.split('  ')[0]] = path.split('  ')[1]
    print("<td><div class='scroll'>")
    for id in path_id:
        url = "https://www.genome.jp/kegg-bin/show_pathway?{}".format(id)
        print('<a href="{}">{}</a>{}'.format(url, id, path_id[id]))
    print("</div></td>")


kegg_id()
