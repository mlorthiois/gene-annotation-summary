import requests

gene=""
url="http://rest.kegg.jp/list/pathway"
r = requests.get(url)
print(r)
if not r.ok:
    ens_url="0"
else:
    decoded = r.json()

print(decoded)
