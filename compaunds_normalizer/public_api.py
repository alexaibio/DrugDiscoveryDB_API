import httpx


class PubChemAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_cid_by_name(self, compound_name: str) -> str:
        return self.__request_cid(compound_name)

    def get_synonyms_by_cid(self, cid: str) -> str:
        result = self.__request_syn(cid)
        return self.__parse_synonyms(result)

    def __request_cid(self, name: str) -> str:
        try:
            # https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/BG8967/cids/TXT
            response = httpx.post(f'{self.base_url}name/{name}/cids/TXT', timeout=None)
            return self.__check_response(response).json()
        except Exception as e:
            raise e

    def __request_syn(self, cid: str) -> dict:
        try:
            # https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/3365/synonyms/TXT
            response = httpx.post(f'{self.base_url}cid/{cid}/synonyms/JSON', timeout=None)
            return self.__check_response(response).json()
        except Exception as e:
            raise e

    def __check_response(self, response: httpx.Response) -> httpx.Response:
        if response.status_code != 200:
            raise
        return response

    def __parse_synonyms(self, response: dict) -> str:
        syn_list = response["InformationList"]["Information"][0]["Synonym"]
        canonical_name = syn_list[0]
        return canonical_name.upper()

