import tkinter as tk
import tkinter.messagebox as msg_box
import querys_mysql as qm
import Aplication_GUI.select_tables_gui as stg
from Aplication_GUI import properties_gui as pg
import os


class ConnectionWindow(tk.Tk, pg.GuiProperties):
    """This class create the first application window: log in to MySQL DB.
    If the log in details are correct then the next window(TableWindow class) is open"""

    pass_counter = 0  # Counter for count the number of clicking Show/Hide button.
    config_file_path = None   # Contain the path to config.ini file.

    def __init__(self):
        super().__init__()
        pg.GuiProperties.__init__(self)

        # Define the reaction of this window, to the user press the window x button.
        self.protocol("WM_DELETE_WINDOW", self.callback)

        # Create label title font=font_style2
        self.label_title = tk.Label(self, text="Please Insert Your \nMySQL Data Setting: ".title(),
                                    font=self.font_style2)
        self.label_title.grid(row=0, sticky='E, S')

        # Create labels
        self.label_host = tk.Label(self, text="Host: ", font=self.font_style2)
        self.label_host.grid(row=1, sticky='W', padx=(160, 0), pady=(50, 0))

        self.label_db = tk.Label(self, text="Database: ", font=self.font_style2)
        self.label_db.grid(row=2, sticky='W', padx=(160, 0), pady=10)

        self.label_user = tk.Label(self, text="User: ", font=self.font_style2)
        self.label_user.grid(row=3, sticky='W', padx=(160, 0), pady=10)

        self.label_pass = tk.Label(self, text="Password: ", font=self.font_style2)
        self.label_pass.grid(row=4, sticky='W', padx=(160, 0), pady=10)

        # Create Entries
        self.host_str = tk.StringVar()
        self.host_str.set("")  # Set the host entry to default text
        self.host_entry = tk.Entry(self, textvar=self.host_str, width=20)
        self.host_entry.grid(row=1, column=1, pady=(50, 0), ipady=3)

        self.db_str = tk.StringVar()
        self.db_str.set("")     # Set the database entry to default text
        self.db_entry = tk.Entry(self, textvar=self.db_str, width=20)
        self.db_entry.grid(row=2, column=1, ipady=3)

        self.user_str = tk.StringVar()
        self.user_str.set("")        # Set the user entry to default text
        self.user_entry = tk.Entry(self, textvar=self.user_str)
        self.user_entry.grid(row=3, column=1, ipady=3)

        self.pass_str = tk.StringVar()
        self.bullet = "\u2022"   # #specifies bullet character
        self.pass_entry = tk.Entry(self, show=self.bullet, textvar=self.pass_str) # Change the password entry to be bullet
        self.pass_entry.grid(row=4, column=1, ipady=3)

        # Create connection button
        conn_button = tk.Button(self, text="Connect", command=self.check_connection, padx=20,
                                activebackground='#4287f5', bd=3)
        tk.Label(self, text='').grid(row=5, column=1)
        conn_button.grid(row=6, column=0, sticky='E', ipadx=10)

        # Create show password button
        self.show_hide_pass_button = tk.Button(self, text="Show", command=self.show_hide_pass,
                                               activebackground='#4287f5', bd=3)
        self.show_hide_pass_button.grid(row=4, column=2, sticky='E', ipadx=5, padx=(20, 0))

    def check_connection(self):
        """
        This method check if the user input are correct, if so, then the user
        get message  and go to the next window.
        :rtype: object
        """
        host = str(self.host_str.get())
        db = str(self.db_str.get())
        user = str(self.user_str.get())
        password = str(self.pass_str.get())

        # Change the directory to config.ini file directory.
        config_dir_path = os.getcwd()
        config_dir_path = config_dir_path.replace('\Aplication_GUI', '')
        os.chdir(config_dir_path)

        # Save this path for future uses
        ConnectionWindow.config_file_path = config_dir_path

        # Change db configuration in config.ini file
        qm.change_db_config(host, db, user, password)
        bool_val = qm.connection_to_db()
        if not bool_val:
            msg = "The connection is failed,\n      Please try again."
            msg_box.showerror("Connection Failed", msg)
        else:
            msg = "The connection succeeded.".title()
            msg_box.showinfo("Connection Succeeded", msg)
            self.destroy()
            stg.TableWindow(ConnectionWindow.config_file_path).mainloop()

    def callback(self):
        """
        This method define the operations that going to \n
        happen before that the application will close off.
        """
        qm.close_connection()  # Close DB connection.
        self.destroy()  # Close the current window.
        exit()  # Close the program.

    def show_hide_pass(self):
        """
        This method change the Show/Hide button text and change the
        password entry to be invisible or visible.
        """
        if ConnectionWindow.pass_counter.__mod__(2) == 0:
            self.pass_entry['show'] = ""
            self.show_hide_pass_button['text'] = "Hide"
            ConnectionWindow.pass_counter +=1
        else:
            self.pass_entry['show'] = self.bullet
            self.show_hide_pass_button['text'] = "Show"
            ConnectionWindow.pass_counter +=1


if __name__ == "__main__":
    window = ConnectionWindow()
    window.mainloop()
