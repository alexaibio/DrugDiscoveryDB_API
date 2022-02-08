from public_api import PubChemAPI

base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
compounds_list = ["Adenosine","Adenocard","BG8967","Bivalirudin","BAYT006267","diflucan","ibrutinib","PC-32765"]

pubchem_api = PubChemAPI(base_url)

# test with one element
cid = pubchem_api.get_cid_by_name(compounds_list[0])
canonical_name = pubchem_api.get_synonyms_by_cid(cid)

# TODO: would be grate to use cache, as dictionary or redis, because API is extreamly slow!
normalized_list = {item: pubchem_api.get_synonyms_by_cid(pubchem_api.get_cid_by_name(item)) for item in compounds_list}

print(normalized_list)














'''
if __name__ == '__main__':
    print_hi('PyCharm')
'''

