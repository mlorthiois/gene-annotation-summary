import requests


def go(uniprot_id, output_file):
    print('\tGo ...')
    go={'function':{},'component':{},'process':{}}
    uniprot_id = uniprot_id[0]
    requestURL = f"https://www.ebi.ac.uk/QuickGO/services/annotation/search?includeFields=goName&geneProductId={uniprot_id}&limit=60"

    r = requests.get(requestURL, headers={ "Accept" : "application/json"}).json()

    for i in r['results']:
        goAspect = i['goAspect']
        goId = i['goId']
        goName = i['goName']
        
        if goAspect == 'molecular_function' and goId not in go['function']:
                go['function'][goId] = goName
        elif goAspect == 'biological_process' and goId not in go['process']:
                go['process'][goId] = goName
        elif goAspect == 'cellular_component' and goId not in go['component']:
                go['component'][goId] = goName

    for feature in go:
        output_file.write('<td><div class="scroll">')
        if go[feature] == {}:
            output_file.write('<i>No data found</i>')
        else:
            for id in go[feature]:
                goName = go[feature][id]
                link = f"http://amigo.geneontology.org/amigo/term/{id}"
                output_file.write(f'<a href={link}>{id}</a> : {goName}</a><br>')
        output_file.write('</div></td>')
            