"""
AlmanachMolecularRepo
"""

import pickle
from pathlib import Path
from typing import Optional, Any
import pandas as pd
from rdkit import Chem
from app.pub_chem_api.pubchem import PubChemAPI
from app.settings import get_project_root


class AlmanacRepo:
    def __init__(self):
        self.__cache_db_df: Optional[Any] = None  # either an object of the specific type is required, or None is required
        self.__chemid_list: Optional[list] = None
        self.__smile_list: dict = {}
        self.__almanach_file = get_project_root() / "DATA_DB/ALMANACH/ComboDrugGrowth_Nov2017.zip"
        self.__cache_file = get_project_root / "files/cache/smile_list.pickle"

    def __load_db_of(self) -> Optional[Any]:
        try:
            filepath = self.__almanach_file
            alm_df = pd.read_csv(filepath, compression='zip', header=0, sep=',')
            alm_df.dropna(inplace=True)
            alm_df = alm_df[['CELLNAME', 'NSC1', 'CONCINDEX1', 'NSC2', 'CONCINDEX2', 'SCORE']]
            alm_df = alm_df.astype({"NSC2": int})
            return alm_df
        except Exception as err:
            print(" ERROR: Cannot open file for ALMANAC!")
            return None

    def __load_smiles(self) -> dict:
        if self.__cache_file.is_file():
            with open(self.__cache_file, 'rb') as handle:
                dict = pickle.load(handle)
        else:
            print("... retrieving smiles from PubChem API")
            dict = {chemid: PubChemAPI().get_canonical_smile_by_cid(str(chemid)) for chemid in self.__chemid_list}
            with open(self.__cache_file, 'wb') as handle:
                pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return dict

    def __validate_alm_db_cache(self):
        if not self.__cache_db_df:
            self.__cache_db_df = self.__load_db_of()
            self.__chemid_list = self.__cache_db_df.NSC1.unique()

        if self.__cache_db_df is None:
            print("ERROR: alm file is not loaded!")
            raise  # Generate an exception here if file error

    def __validate_smile_api_cache(self):
        if not self.__smile_list:
            self.__smile_list = self.__load_smiles()

    def get_alm_data(self, cell_line: str = None, use_cache: bool = True):
        print(f' Retrieving ALMANAC data for the [{cell_line if cell_line else " WHOLE "}] dataset')
        self.__validate_alm_db_cache()
        if use_cache:
            df = self.__cache_db_df.copy() # можно использовать глубокое копирование, и тогда загружать данные не надо будет, оно работает быстро и кэш всегда будет валидным, но все ависит от бъемов данных
        df = self.__load_db_of()
        return df[df.CELLNAME==cell_line] if cell_line else df

    def get_alm_chemid_list(self):
        return self.__chemid_list

    def get_smile_of(self, chemid: int) -> str:
        self.__validate_smile_api_cache()
        return self.__smile_list[chemid]

# import molecular objects from ALMANAC for 104 drugs
# TODO: remove it, dont use it now
all_fda_compounds = Chem.SDMolSupplier('../app/DATA_DB/ALMANACH/2D_struct_ComboCompoundSet.sdf')


if __name__ == "__main__":
    alm = AlmanacRepo()
    data = alm.get_alm_data()
    id_list = alm.get_alm_chemid_list()
    smile = alm.get_smile_of(752)
    print(smile)

