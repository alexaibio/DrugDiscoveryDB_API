# TODO: better from here - https://www.cancerrxgene.org/downloads/anova
from dataclasses import dataclass
import csv
from csv import DictReader
from typing import Optional, List, Dict

@dataclass
class CellLine:
    broad_id: str
    sanger_id: str
    alias: str
    ccle_name: Optional[str]
    disease: str
    disease_subtype: str
    gender: str
    source: Optional[str]


class CellLineData:
    def __init__(self, path):
        # TODO: add singlton !!
        self._db: Dict = self.__create_cell_lines_db(path)

    def __create_cell_lines_db(self, path: str) -> dict:
        cell_lines_dict = {}
        with open(path, 'r') as f:
            csv_dict_reader = DictReader(f)
            csv_reader = csv.reader(f, delimiter=",")  # get column names from a csv file
            column_names = csv_dict_reader.fieldnames

            for row in csv_reader:  # For each row in the csv file
                cl = CellLine(
                    broad_id=row[0],
                    sanger_id=row[4],
                    alias=row[2],
                    ccle_name=row[1],
                    disease=row[5],
                    disease_subtype=row[6],
                    gender=row[7],
                    source=row[8]
                )
                cell_lines_dict[cl.alias] = cl

        return cell_lines_dict

    def __getitem__(self, item):
        return self._db.get(item, None)


if __name__ == "__main__":
    db = CellLineData('DepMap-2018q3-celllines.csv')
    rec = db['A498']
    print(rec)

