import write_excel_file as wef
import querys_mysql as qm

if __name__ == '__main__':
    # This section is just for execute the code, and generate the excel tables in Command Line way

    val = input("Press 1 for change mysql configuration, Else, press 2: ".title())
    if val == str(1):
        host = input("Insert host: ".title())
        database = input("Insert database: ".title())
        user = input("Insert user: ".title())
        password = input("Insert password: ".title())
        qm.change_db_config(host, database, user, password)

    val = qm.connection_to_db()
    if val is False:
        print('Connection failed.')
        exit(0)
    wef.create_new_directory()
    wef.change_dir()

    # get all the tables names in the db.
    table_names_list = qm.run_db_query("SHOW TABLES;")

    # for every table create excel file.
    for element in table_names_list:
        table_name = str(element[0])

        # create excel file for this table.
        excelFile = wef.createExcelFile(table_name + '_table.xlsx')

        # create mySQL query to bring all the table data.
        query = qm.create_query(table_name)
        data = qm.run_db_query(query)

        table_info = qm.get_table_column_info(table_name)
        wef.write_to_excel_file(excelFile, data, table_info)
        excelFile.close()
        break
    qm.close_connection()


def create_excel_table(tables_names_list):
    # for every table name in the list create excel file with table.
    for element in tables_names_list:
        table_name = str(element[0])

        # create excel file for this table.
        excelFile = wef.createExcelFile(table_name + '_table.xlsx')

        # create mySQL query to bring all the table data.
        query = qm.create_query(table_name)
        data = qm.run_db_query(query)

        table_info = qm.get_table_column_info(table_name)
        wef.write_to_excel_file(excelFile, data, table_info)
        excelFile.close()
    return True
