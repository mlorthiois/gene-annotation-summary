import requests


def go(uniprot_id, output_file):
    """Find features in the Go database from UniprotKB IDs.

    Find go features (molecular function, biological process and cellular
    component) of a protein, and write them in 3 columns of a HTML table.

    Args:
        uniprot_id (list)
        output_file (open file) : file to write in.
    """
    print('\tGo ...')

    domain = "https://www.ebi.ac.uk/QuickGO/services/"
    search = "annotation/search?includeFields=goName"
    requestURL = f"{domain}{search}&geneProductId={uniprot_id[0]}&limit=60"
    headers = {"Accept": "application/json"}
    r = requests.get(requestURL, headers=headers).json()

    # Parse the json and add features in the go dic according to the type
    go = {'function': {}, 'component': {}, 'process': {}}
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

    # Write each go feature in a different col
    for feature in go:
        output_file.write('<td><div class="scroll">')
        if go[feature] == {}:
            output_file.write('<i>No data found</i>')
        else:
            for id in go[feature]:
                goName = go[feature][id]
                link = f"http://amigo.geneontology.org/amigo/term/{id}"
                output_file.write(f'<a href={link}>{id}</a>: {goName}</a><br>')
        output_file.write('</div></td>')
