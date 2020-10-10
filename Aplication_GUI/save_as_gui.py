import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as msg_box
import write_excel_file as wef
import os
import Aplication_GUI.select_tables_gui as stg


class SaveAs(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Hide jumping window.
        self.withdraw()

        while True:
            # Get the path of the given directory.
            self.directory_path = filedialog.askdirectory()
            status = self.check_dir_empty()
            if not status:
                msg = "Directory is not empty.".title()
                msg_box.showerror("Directory Failed", msg)
            else:
                SaveAs.change_directory()

                # Update the .INI file th store the given directory path.
                wef.update_ini_file(self.directory_path)
                break

    def check_dir_empty(self):
        if len(os.listdir(self.directory_path)) == 0:
            return True
        return False

    @staticmethod
    def change_directory():
        # Change the directory to config.ini file directory.
        config_dir_path = os.getcwd()
        config_dir_path = config_dir_path.replace('\Aplication_GUI', '')
        os.chdir(config_dir_path)


if __name__ == "__main__":
    SaveAs()
