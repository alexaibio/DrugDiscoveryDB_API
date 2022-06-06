# https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/122758/property/MolecularFormula/txt
# https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/122758/property/CanonicalSMILES/txt
# source - https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest$_Toc494865556
import httpx


class PubChemAPI:
    def __init__(self, base_url: str = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"):
        self.base_url = base_url

    def get_cid_by_name(self, compound_name: str) -> str:
        return self.__api_request_cid(compound_name)

    def get_canonical_name_by_cid(self, cid: str) -> str:
        result = self.__api_request_synonyms(cid)
        syn_dict = self.__parse_synonyms(result)
        return syn_dict[0].upper()

    def get_all_synonyms_by_cid(self, cid: str) -> list:
        result = self.__api_request_synonyms(cid)
        syn_dict = self.__parse_synonyms(result)
        return list(syn_dict)

    def get_canonical_smile_by_cid(self, cid: str) -> str:
        return self.__api_request_canonical_smile(cid)

    def __api_request_cid(self, name: str) -> str:
        try:
            # https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/BG8967/cids/TXT
            response = httpx.post(f'{self.base_url}name/{name}/cids/TXT', timeout=None)
            return self.__check_response(response).json()
        except Exception as e:
            raise e

    def __api_request_synonyms(self, cid: str) -> dict:
        try:
            # https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/3365/synonyms/TXT
            response = httpx.post(f'{self.base_url}cid/{cid}/synonyms/JSON', timeout=None)
            return self.__check_response(response).json()
        except Exception as e:
            raise e

    def __api_request_canonical_smile(self, cid: str) -> str:
        try:
            # https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/122758/property/CanonicalSMILES/txt
            response = httpx.post(f'{self.base_url}cid/{cid}/property/CanonicalSMILES/TXT', timeout=None)
            return (self.__check_response(response).text).strip('\n')
        except Exception as e:
            raise e

    def __check_response(self, response: httpx.Response) -> httpx.Response:
        if response.status_code != 200:
            raise Exception(f'PubChen API bad respone (no chemical?) {response.status_code}')
        return response

    def __parse_synonyms(self, response: dict) -> str:
        syn_list = response["InformationList"]["Information"][0]["Synonym"]
        return syn_list

if __name__ == "__main__":
    pb = PubChemAPI()
    print(pb.get_cid_by_name(compound_name='erythromycin'))