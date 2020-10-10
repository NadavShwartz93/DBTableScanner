import xlsxwriter
import os
import shutil
import datetime
from configparser import ConfigParser


def createExcelFile(file_name='hello.xlsx'):
    """The method create new excel file.\n
    :param file_name: is the name of the file.
    :return: instance of the created file.
    """
    # Check if file exists, then delete it:
    if os.path.exists(file_name):
        os.remove(file_name)
    workbook = xlsxwriter.Workbook(file_name)
    print("Excel file creation succeeded!")
    return workbook


def create_new_directory():
    """
    This method get user directory path.
    """
    location = input("Please enter directory path: ".title())
    dir_name = input("Please enter directory name: ".title())

    get_answer = input("directory content will be override, for cancel enter 1: ".title())
    while True:
        if get_answer != str(1):
            path = os.path.join(location, dir_name)
            path = path.replace('\\', '//')

            if not os.path.exists(path):
                os.makedirs(path)
            else:
                shutil.rmtree(path)
                os.makedirs(path)
            break
        else:
            location = input("Please enter directory path:".title())
            dir_name = input("Please enter directory name:".title())
            get_answer = input("directory content will be override, for cancel enter 1:".title())
    # update the .ini file about the new directory location and name.
    update_ini_file(path)


def update_ini_file(dir_path, filename='config.ini'):
    """
    This dir_path will contain all the excel files.\n
    The method will change the .ini file: update the 'directory' section.\n
    :param filename:
    :param dir_path: is the directory path that will contain all the excel files.
    """
    config = ConfigParser()
    # parse existing file
    config.read(filename)
    config.set('directory', 'directory_path', dir_path)

    with open(filename, 'w') as configfile:
        config.write(configfile)


def change_dir(filename='config.ini'):
    """
    This method change the current directory,
    in order to save all the excel files in the user selected directory.
    """
    path = get_directory_path(filename)
    os.chdir(path)


def write_to_excel_file(excel_file, data, table_info):

    worksheet_name = str(datetime.date.today())
    worksheet = excel_file.add_worksheet(worksheet_name)

    # Prepare the table options values
    table_size = get_table_size(data, table_info)
    # Get the table first column char.
    table_first_col = table_size[0]
    table_col = get_table_col_info(table_info, excel_file, worksheet, table_first_col)
    final_table_data = merge_lists(data, table_info)
    table_name = str(excel_file.filename).replace('.xlsx', '')
    worksheet.col_size_changed = True

    options = {
        'data': final_table_data, 'columns': table_col, 'autofilter': False,
        'banded_rows':False, 'banded_columns':False, 'style':'Table Style Medium 13',
        'name':table_name
    }
    # Insert the table and all its content to the excel file.
    worksheet.add_table(table_size, options)

    print("{} written successfully!".format(excel_file.filename))


def get_table_col_info(table_info, excel_file, worksheet, table_first_col):
    """
    The method create list of dictionaries: for every table column create {'header': 'table_column_name'}.\n
    :param table_info: list of list of that contain column names and column types of the given table.
    :param worksheet:
    :param table_first_col:
    :return: list of dictionaries (Example: [{'header': 'table_column1_name'}, ..., {'header': 'table_columnN_name'}] )
    """
    header = 'header'
    temp_list = []
    temp_dict = dict()
    temp_dict[header] = 'Column Name:'
    temp_list.append(temp_dict)

    column_num = convert_col_chr_to_num(table_first_col)-1
    set_column_width(worksheet, column_num, 'Column Name:')

    column_num += 1
    for x in table_info:
        temp_dict = dict()
        temp_dict[header] = x[0]

        # Add format to column according to column dataType.
        if x[1] == 'time':
            time_format = set_col_format(excel_file, 21)
            temp_dict['format'] = time_format
        elif x[1] == 'timestamp':
            time_format = set_col_format(excel_file, 22)
            temp_dict['format'] = time_format

        temp_list.append(temp_dict)

        # Change column width
        set_column_width(worksheet, column_num, x[0])
        column_num += 1

    return temp_list


def set_col_format(excel_file, format_num: int):
    format_inst = excel_file.add_format()
    format_inst.set_num_format(format_num)
    return format_inst


def get_table_size(data, table_info):
    """
    The method calc the table size(Example: 'B3:D7')\n
    :param data: list of list with the data that the  mySQL table content.
    :param table_info: list of list of that contain column names and column types of the given table.
    :rtype: string that contain the table size.
    """
    y_start = 3
    y_end = len(data) + 4
    x_start = 'B'

    ascii_val = ord(x_start) + len(table_info)
    x_end = chr(ascii_val)
    table_size = str(x_start) + str(y_start) + ':' + x_end + str(y_end)
    return table_size


def merge_lists(data, table_info):
    """
    The method merge data list with the column types that is store in table_info list.\n
    :param data: list of list with the data of the mySQL table content.
    :param table_info: list of list with the content column names and column types of the given table.
    :return: list of list that contain the final data that will be written.
    """
    final_table_data = []
    tmp_list = list()

    # handle the first table row: this row contain the data type of every column.
    tmp_list.append("Data Type:")
    for x in table_info:
        tmp_list.append(x[1])
    final_table_data.append(tmp_list)

    # Cope the contact of data list into
    for x in data:
        x.insert(0, "")
        final_table_data.append(x)
    return final_table_data


def convert_col_chr_to_num(table_col_chr):
    """
    This method get char that represent the table column,\n
    and return the number that this column represent.\n
    :param table_col_chr: is char that represent the table column.
    :return: the number that represent the table column
    """
    if len(table_col_chr) ==  1:
        col_num = ord(table_col_chr)
        # 64 represent the number needed for subtraction from decimal ASCII value
        # in order to get the column number.
        # Example: table_col_chr = 'A' decimal ASCII value = 65 --> 65 - 64 = 1
        col_num = col_num - 64
        return col_num
    else:#TODO: The case the table_col_chr is bigger then 1
        pass


def set_column_width(worksheet, table_first_col_num, col_name):
    """
    This method change the column width for every given column number.\n
    :param worksheet: is worksheet instance.
    :param table_first_col_num: is the number that represent the column number.
    :param col_name: is the name of the table column.
    """
    col_width = 15
    if len(col_name) > col_width:
        worksheet.set_column(table_first_col_num,table_first_col_num, len(col_name)+1)
    else:
        worksheet.set_column(table_first_col_num,table_first_col_num, col_width)


def get_directory_path(filename='config.ini'):
    """This method get the selected directory path from the config.ini file."""
    config = ConfigParser()
    config.read(filename)

    # Get the path of the directory that will contain all the DB tables
    path = config.get('directory', 'directory_path')
    return path



