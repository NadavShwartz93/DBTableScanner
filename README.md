# DBTableScanner
Scan MySQL db table into Excel table formate.
![](VideoOfTheProject.gif)

# Overview
Nice tool for scan DB MySQL table into Excel table.


# Project technologies:
Technologies | Version
------------ | -------------
**Python** | 3.7.9
**tkinter** | 8.6 
[xlsxwriter](https://pypi.org/project/XlsxWriter/) | 1.3.6

**All the project development has be done with \
IntelliJ IDEA 2020.2.3 (Community Edition).**

# Operating instructions
* Run [connection_gui.py](Aplication_GUI/connection_gui.py) that generated [ConnectionWindow](Aplication_GUI/ConnectionWindow.png)
* Insert MySQL connection details: host, user, database name, password.
* Press connect button.
* If connected successfully, and [querys_mysql.py](querys_mysql.py) done some important stuff, then \
  select table from [SelectTableWindow](Aplication_GUI/SelectTableWindow.png).
* Press Create Table button and [write_excel_file.py](write_excel_file.py) will create the table in Excel.
* Select empty directory path to save the Excel files into.
* The selected directory path window will be open with the generated files.
