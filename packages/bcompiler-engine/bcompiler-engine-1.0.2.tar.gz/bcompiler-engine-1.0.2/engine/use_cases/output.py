"""
Use cases related to writing data to an output repository.
"""

import logging
import string
import warnings
from pathlib import Path
from typing import List

from openpyxl import load_workbook

from engine.repository.datamap import InMemorySingleDatamapRepository
from engine.use_cases.parsing import ParseDatamapUseCase
from engine.use_cases.typing import (MASTER_COL_DATA, MASTER_DATA_FOR_FILE,
                                     ColData)

warnings.filterwarnings("ignore", ".*Conditional Formatting*.")
warnings.filterwarnings("ignore", ".*Sparkline Group*.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
logger = logging.getLogger(__name__)


class WriteMasterToTemplates:
    """
    Re-creation of the old bcompiler -a functionality.

    Writes data from a given master to a blank template and saves each file according
    to each relevant column in the master.
    """

    def __init__(self, output_repo, datamap: Path, master: Path, blank_template: Path):
        self.output_repo = output_repo
        self._datamap = datamap
        self._master_path = master
        self._master_sheet = load_workbook(master).active
        self._blank_template = blank_template
        self._col_a_vals: List[str]

    def _check_datamap_matches_cola(self) -> bool:
        parsed_dm_data = self._parse_dm_uc.execute(obj=True)
        self._dml_line_tup = [(x.key, x.sheet, x.cellref) for x in parsed_dm_data]
        self._col_a_vals = []
        for cell in next(self._master_sheet.columns):
            try:
                self._col_a_vals.append(cell.value.strip())
            except AttributeError:
                self._col_a_vals.append("EMPTY")
        self._col_a_vals = self._col_a_vals[1:]
        _pass = zip([x[0] for x in self._dml_line_tup], self._col_a_vals)
        return all([x[0] == x[1] for x in _pass])

    def _get_keys_in_datamap_not_in_master(self) -> List[str]:
        dm_keys_s = set([x[0] for x in self._dml_line_tup])
        master_keys_s = set(self._col_a_vals)
        return list(dm_keys_s - master_keys_s)

    def execute(self) -> None:
        """
        Writes a master file to multiple templates using blank_template,
        based on the blank_template and the datamap.
        """

        master_data: MASTER_DATA_FOR_FILE = []

        self.parse_dm_repo = InMemorySingleDatamapRepository(str(self._datamap))
        self._parse_dm_uc = ParseDatamapUseCase(self.parse_dm_repo)
        if not self._check_datamap_matches_cola():
            _missing_keys = self._get_keys_in_datamap_not_in_master()
            # You shall not pass if this is a problem
            if _missing_keys:
                for m in _missing_keys:
                    logger.critical(
                        f"Key {m} in the datamap but not in the master. Not continuing."
                    )
                raise RuntimeError(
                    "Not continuing. Ensure all keys from datamap are in the master."
                )
        cola = [x.value for x in list(self._master_sheet.columns)[0]][1:]
        for col in list(self._master_sheet.columns)[1:]:
            tups = []
            # temp fix for https://github.com/hammerheadlemon/datamaps/issues/5
            try:
                file_name = col[0].value.split(".")[0]
            except AttributeError:
                _col_des = string.ascii_uppercase[col[0].column - 1]
                _row_des = str(col[0].row)
                _cell_coords = "".join([_col_des, _row_des])
                logger.warning(
                    f"Cell {_cell_coords} value is empty. Expected a value here. Likely error in master causing column "
                    f"boundary to be overrun. Continuing, but resulting file may be unstable. Copy your master data to a new file and rerun.")
                continue
            # end of temp fix
            logger.info(f"Extracting data for {file_name} from {self._master_path}")
            for i, key in enumerate(cola, start=1):
                key = key.strip()
                try:
                    sheet = [dml[1] for dml in self._dml_line_tup if dml[0] == key][0]
                except IndexError:
                    continue
                cd = ColData(
                    key=key,
                    sheet=sheet,
                    cellref=[dml[2] for dml in self._dml_line_tup if dml[0] == key][0],
                    value=col[i].value,
                    file_name=file_name,
                )
                tups.append(cd)
            master_data.append(tups)

        self.output_repo.write(master_data, from_json=False)
