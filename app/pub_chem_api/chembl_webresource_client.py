# https://github.com/chembl/chembl_webresource_client
from chembl_webresource_client.new_client import new_client

# find a molecule by its synonyms
molecule = new_client.molecule
mols = molecule.filter(molecule_synonyms__molecule_synonym__iexact='viagra').only('molecule_chembl_id')
mols


# Get a single molecule by ChEMBL id
molecule = new_client.molecule
m1 = molecule.filter(chembl_id='CHEMBL192').only(['molecule_chembl_id', 'pref_name', 'molecule_structures'])
m1

# Get a single molecule by standard inchi key
molecule = new_client.molecule
mol = molecule.filter(molecule_structures__standard_inchi_key='BSYNRYMUTXBXSQ-UHFFFAOYSA-N').only(['molecule_chembl_id', 'pref_name', 'molecule_structures'])
mol


# Get all approved drugs
molecule = new_client.molecule
approved_drugs = molecule.filter(max_phase=4).order_by('molecule_properties__mw_freebase')
approved_drugs


# Get all IC50 activities related to the hERG target
target = new_client.target
activity = new_client.activity
herg = target.filter(pref_name__iexact='hERG').only('target_chembl_id')[0]
herg_activities = activity.filter(target_chembl_id=herg['target_chembl_id']).filter(standard_type="IC50")
len(herg_activities)

#Get cell line by cellosaurus id
cell_line = new_client.cell_line
res = cell_line.filter(cellosaurus_id="CVCL_0417")
res

# Find a target by gene name
target = new_client.target
gene_name = 'BRD4'
res = target.filter(target_synonym__icontains=gene_name).only(['organism', 'pref_name', 'target_type'])
for i in res:
    print(i)



