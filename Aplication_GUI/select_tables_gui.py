import tkinter as tk
import tkinter.messagebox as msg_box
import querys_mysql as qm
import write_excel_file as wef
import Excel_tables_creators
from Aplication_GUI import properties_gui as pg
import Aplication_GUI.save_as_gui as sag
import Aplication_GUI.connection_gui as cg
import os


ROWS, COLS = 8, 6  # Size of grid.
ROWS_DISP = 7  # Number of rows to display.
COLS_DISP = 4  # Number of columns to display.


def change_directory():
    # Change the directory to config.ini file directory.
    current_directory = os.getcwd()
    current_directory = current_directory.replace('\Aplication_GUI', '')
    os.chdir(current_directory)


class TableWindow(tk.Tk, pg.GuiProperties):
    def __init__(self):
        tk.Tk.__init__(self)
        pg.GuiProperties.__init__(self)

        # Define the reaction of this window, to the user press the window x button.
        self.protocol("WM_DELETE_WINDOW", self.callback)

        # Create master frame.
        master_frame = tk.Frame(self, relief=tk.RIDGE)
        master_frame.grid(sticky=tk.NSEW)

        # Create Label title.
        self.label_title = tk.Label(master_frame, text="Please select \ntable to scan: ".title(), font=self.font_style2)
        self.label_title.grid(row=0, column=0, sticky=tk.NW)
        tk.Label(master_frame, text='').grid(row=1)

        # Create a frame for the canvas and scrollbar(s).
        frame1 = tk.Frame(master_frame, bd=2)
        frame1.grid(row=2, sticky=tk.NSEW)

        # Create canvas and add it into frame.
        self.canvas = tk.Canvas(frame1, bg="white", width=pg.WIDTH_SIZE)
        self.canvas.grid(row=0)

        # Create a vertical scrollbar linked to the canvas.
        vsbar = tk.Scrollbar(frame1, orient=tk.VERTICAL, command=self.canvas.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)
        self.canvas.configure(yscrollcommand=vsbar.set)

        # Create a horizontal scrollbar linked to the canvas.
        hsbar = tk.Scrollbar(frame1, orient=tk.HORIZONTAL, command=self.canvas.xview)
        hsbar.grid(row=1, column=0, sticky=tk.EW)
        self.canvas.configure(xscrollcommand=hsbar.set)

        # Create a frame on the canvas to contain the checkbutton.
        checkbutton_frame = tk.Frame(self.canvas, bg="white", bd=2)

        # The connection to DB made in the previous window: connection_gui.py
        self.table_names_list = qm.run_db_query("SHOW TABLES;")
        self.checkbutton_list = list()

        row_index = 2
        col_index = 0
        index = 1
        # Create Checkbutton(checkbox) for every database table.
        for element in self.table_names_list:
            table_bool = tk.IntVar()
            table_name = str(element[0])
            temp_dict = dict()
            c = tk.Checkbutton(checkbutton_frame, variable=table_bool, text=table_name, font=self.font_style3)

            # Add dictionary to the list {key=table_name, value=True/False}
            temp_dict[table_name] = table_bool
            self.checkbutton_list.append(temp_dict)
            if index.__mod__(ROWS):
                c.grid(row=row_index, column=col_index, sticky=tk.W, padx=(5, 20))
                row_index += 1
                index += 1
            else:
                c.grid(row=row_index, column=col_index, sticky=tk.W, padx=(5, 20))
                row_index = 2
                col_index += 1
                index += 1

        # Create canvas window to hold the buttons_frame.
        self.canvas.create_window((0, 0), window=checkbutton_frame, anchor=tk.NW)

        checkbutton_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = self.canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        # Define the scrollable region as entire canvas with only the desired
        # number of rows and columns displayed.
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)
        self.canvas.configure(scrollregion=bbox, width=dw, height=dh)

        # Create a frame for the buttons.
        frame2 = tk.Frame(master_frame, bd=2)
        frame2.grid(row=3, sticky=tk.NSEW, pady=(20, 0))

        # Create 3 buttons: 1.Button for: "Create All Tables",
        # 2.Button for: "Create Tables" that create only the selected tables,
        # 3.Button for: "Select All Tables" that select all the checkbutton.
        all_tables_button = tk.Button(frame2, text="Create All Tables", command=self.create_all_tables, bd=3,
                                      activebackground='#4287f5')
        all_tables_button.grid(row=0, column=0, sticky=tk.E, ipadx=10, padx=(30, 0))

        tables_button = tk.Button(frame2, text="Create Tables ", command=self.create_tables, bd=3,
                                  activebackground='#4287f5')
        tables_button.grid(row=0, column=1, sticky=tk.E, ipadx=10, padx=(90, 100))

        select_all_button = tk.Button(frame2, text="Select All Tables", command=self.select_all_checkbutton, bd=3,
                                      activebackground='#4287f5')
        select_all_button.grid(row=0, column=2, sticky=tk.E, ipadx=10, padx=(0, 0))

    def create_all_tables(self):
        # Open the save as dialog window
        sag.SaveAs()
        # Change the current directory to the user input
        wef.change_dir()
        val_bool = Excel_tables_creators.create_excel_table(self.table_names_list)
        self.msg_for_user(val_bool)

    def create_tables(self):
        tables_names = []
        for elem in self.checkbutton_list:
            for key, value in elem.items():
                if value.get() == 1:
                    temp_list = list()
                    temp_list.append(key)
                    tables_names.append(temp_list)

        # Open the save as dialog window
        sag.SaveAs()
        # Change the current directory to the user input
        wef.change_dir()
        val_bool = Excel_tables_creators.create_excel_table(tables_names)
        self.msg_for_user(val_bool)

    def select_all_checkbutton(self):
        for elem in self.checkbutton_list:
            for key, value in elem.items():
                value.set(1)

    def callback(self):
        self.destroy()
        cg.ConnectionWindow().mainloop()

    @staticmethod
    def msg_for_user(val_bool):
        if val_bool:
            msg = "Excel file creation succeeded!".title()
            msg_box.showinfo("Succeeded", msg)
