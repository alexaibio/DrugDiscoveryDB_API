from dataclasses import dataclass, field
import csv
from csv import DictReader
from typing import Optional, List, Dict
from itertools import count


@dataclass
class DrugCombination:
    cell_line: str
    cl_cosmic_id: str
    cl_tissue: str
    cl_cancer_type: str
    drug1: str
    drug2: str
    drug3: str
    interaction: str
    reference: str
    dc_id: int = field(default_factory=count().__next__)


class DrugCombData:
    def __init__(self, path):
        # TODO: add singlton !!
        self._db: Dict = self.__create_drug_combinations_db(path)

    def __create_drug_combinations_db(self, path: str) -> dict:
        drug_comb_dict = {}
        with open(path, 'r', encoding='utf-8-sig') as f:
            csv_dict_reader = DictReader(f, delimiter=",")
            #csv_reader = csv.reader(f, delimiter=",")  # get column names from a csv file

            for row in csv_dict_reader:  # For each row in the csv file
                dc = DrugCombination(
                    cell_line=row['Cell Line'],
                    cl_cosmic_id=row['Cosmic_ID'],
                    cl_tissue=row['Tissue'],
                    cl_cancer_type=row['Cancer-type'],
                    drug1=row['Drug1'],
                    drug2=row['Drug2'],
                    drug3=row['Drug3'],
                    interaction=row['Note'],
                    reference=f'Pubmed: {row["Pubmed ID"]}, article: {row["Reference"]}'
                )
                drug_comb_dict[dc.dc_id] = dc

        return drug_comb_dict

    def __getitem__(self, item):
        return self._db.get(item, None)

    def get_drug_combinations_as_list(self) -> list:
        return list(self._db.values())

    def get_pure_synergistic_combinations(self) -> list:
        return [ v for v in self._db.values() if v.interaction.lower() in ['synergy', 'synergistic'] ]


if __name__ == "__main__":
    db = DrugCombData('41467_2020_16735_MOESM5_ESM.csv')
    db_pure = db.get_pure_synergistic_combinations()
    print(db[0])
    print(db[1])


