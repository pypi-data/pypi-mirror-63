from abc import ABCMeta, abstractmethod
from ExcelDataDriver.ExcelTestDataRow.MandatoryTestDataColumn import MANDATORY_TEST_DATA_COLUMN
from openpyxl.utils import column_index_from_string
from openpyxl.utils.cell import coordinate_from_string


class ABCParserStrategy:

    __metaclass__ = ABCMeta

    def __init__(self, main_column_key):
        self.MANDATORY_TEST_DATA_COLUMN = MANDATORY_TEST_DATA_COLUMN
        self.DEFAULT_COLUMN_INDEXS = self.MANDATORY_TEST_DATA_COLUMN.values()
        self.start_row = 1
        self.max_column = 50
        self.maximum_column_index_row = 5
        self.main_column_key = main_column_key

    def is_ws_column_valid(self, ws, validate_result):
        ws_column_indexes = self.parsing_column_indexs(ws)
        diff_column_list = list(set(self.DEFAULT_COLUMN_INDEXS) - set(ws_column_indexes))
        if len(diff_column_list) > 0:
            validate_result['is_pass'] = False
            validate_result['error_message'] += "[" + ws.title + "] Excel column " + ", ".join(
                diff_column_list) + " are missing.\r\n"
            print("[" + ws.title + "] Excel column " + ", ".join(diff_column_list) + " are missing.")
        return validate_result

    @abstractmethod
    def is_test_data_valid(self, ws_column_indexes, ws_title, row_index, row): pass

    @abstractmethod
    def map_data_row_into_test_data_obj(self, ws_column_indexes, ws_title, row_index, row): pass

    def get_all_worksheet(self, wb):
        return list(wb)

    def parsing_column_indexs(self, ws):
        ws_column_indexs = {}
        # Parse mandatory property
        for index, row in enumerate(ws.rows):
            if index > self.maximum_column_index_row:
                break
            for cell in row:
                if (cell.value is not None) and (cell.value in self.DEFAULT_COLUMN_INDEXS):
                    ws_column_indexs[cell.value] = column_index_from_string(coordinate_from_string(cell.coordinate)[0])
                    print('Mandatory : '+str(cell.value) + ' : ' + str(cell.coordinate) + ' : ' + str(column_index_from_string(coordinate_from_string(cell.coordinate)[0])))
                    self.start_row = index + 1
            if len(ws_column_indexs) > 0:
                break

        # Parse optional property
        for index, row in enumerate(ws.rows):
            if index > self.maximum_column_index_row:
                break
            if index != self.start_row - 1:
                continue
            for cell in row:
                if (cell.value is not None) and (cell.value not in self.DEFAULT_COLUMN_INDEXS):
                    field_name = str(cell.value).lower().strip().replace(" ", "_")
                    ws_column_indexs[field_name] = column_index_from_string(coordinate_from_string(cell.coordinate)[0])
                    print('Optional : '+field_name + ' : ' + str(cell.coordinate) + ' : ' + str(column_index_from_string(coordinate_from_string(cell.coordinate)[0])))
            break
        print('Done parsing column indexes')
        return ws_column_indexs

    def parse_test_data_properties(self, ws, ws_column_indexs):
        test_datas = []
        for index, row in enumerate(ws.rows):
            if index < self.start_row:
                continue
            self.is_test_data_valid(ws_column_indexs, ws.title, index, row)
            test_data = self.map_data_row_into_test_data_obj(ws_column_indexs, ws.title, index, row)
            if test_data is not None:
                test_datas.append(test_data)
            else:
                break
        print('Total test datas: ' + str(len(test_datas)))
        return test_datas

