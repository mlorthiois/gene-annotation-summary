import requests
ID="P35829"
url = 'https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq=P35829&output=json'
r = requests.get(url)
r = r.json()
if r['n_match']==0:
    print('Error')