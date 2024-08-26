import multiprocessing

import customtkinter
from CTkTable import *
from PIL import Image
from tkinter import ttk


from create_logger import setup_logger

BACKGROUND_IMAGE = "UI/background.jpg"



class APP(customtkinter.CTk):
    """Class for the main GUI window."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.geometry("1100x700")
        self.attributes('-topmost', 1)
        self.title("OPC UA Server")

        self.widget_height = 40
        self.widget_width = 190
        self.font_size = 20
        self.font=customtkinter.CTkFont(size=18)

        self.status = "Stopped"

        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (self.winfo_width() / 2)
        y_coordinate = (screen_height / 2) - (self.winfo_height() / 2)
        self.geometry(f"+{int(x_coordinate)}+{int(y_coordinate)}")
        self.resizable(False, False)

        self.frame = customtkinter.CTkFrame(master=self, bg_color="transparent")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=1)
        self.frame.columnconfigure(5, weight=1)
        self.frame.columnconfigure(6, weight=2)
        self.frame.columnconfigure(7, weight=2)
        self.frame.columnconfigure(8, weight=2)
        self.frame.columnconfigure(9, weight=3)
        self.frame.columnconfigure(10, weight=3)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.frame.grid_rowconfigure(5, weight=1)
        self.frame.grid_rowconfigure(6, weight=1)
        self.frame.grid_rowconfigure(7, weight=1)
        self.frame.grid_rowconfigure(8, weight=1)
        self.frame.grid_rowconfigure(9, weight=1)
        self.frame.grid_rowconfigure(10, weight=2)

        self.button_setting = customtkinter.CTkButton(master=self.frame,
                                                 command=self.temp,
                                                 text="Settings",
                                                 width=self.widget_width,
                                                 height=self.widget_height,
                                                 font=self.font)
        self.button_setting.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.button_start_server = customtkinter.CTkButton(master=self.frame,
                                                 command=self.temp,
                                                 text="Start Server",
                                                 width=self.widget_width,
                                                 height=self.widget_height,
                                                 font=self.font)
        self.button_start_server.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.label_status = customtkinter.CTkLabel(master=self.frame, justify=customtkinter.CENTER,
                                            text=(f"Server Status: {self.status}"),
                                            font=customtkinter.CTkFont(size=20, weight="bold"),
                                            bg_color="transparent",
                                            width=self.widget_width,
                                            height=self.widget_height)
        self.label_status.grid(row=0, column=1, sticky="w", columnspan=1)

        self.entry_event_name = customtkinter.CTkEntry(master=self.frame,
                                                  placeholder_text="Event Name",
                                                  width=self.widget_width,
                                                  height=self.widget_height,
                                                  font=self.font)
        self.entry_event_name.grid(row=3, column=0, padx=10, pady=(40,10), sticky="ew")

        self.entry_event_message = customtkinter.CTkEntry(master=self.frame,
                                                     placeholder_text="Event Message",
                                                     width=self.widget_width,
                                                     height=self.widget_height,
                                                     font=self.font)
        self.entry_event_message.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.entry_event_severity = customtkinter.CTkEntry(master=self.frame,
                                                      placeholder_text="Event Severity",
                                                      width=self.widget_width,
                                                      height=self.widget_height,
                                                      font=self.font)
        self.entry_event_severity.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.entry_event_reacurring = customtkinter.CTkEntry(master=self.frame,
                                                        placeholder_text="Event reacurring in sec.",
                                                        width=self.widget_width,
                                                        height=self.widget_height,
                                                        font=self.font)
        self.entry_event_reacurring.grid(row=6, column=0, padx=10, pady=10, sticky="ew", columnspan=1)

        self.button_add_event = customtkinter.CTkButton(master=self.frame,
                                                 command=self.add_event,
                                                 text="Add Event",
                                                 width=self.widget_width,
                                                 height=self.widget_height,
                                                 font=self.font)
        self.button_add_event.grid(row=7, column=0, padx=10, pady=0, sticky="ew")

        #self.frame_event_display = CTkXYFrame(self.frame, width=600, height=400)
        #self.frame_event_display.grid(row=3, column=3, padx=10, pady=10, sticky="ew", columnspan=10, rowspan=10)


        style = ttk.Style()

        style.theme_use("default")

        style.configure("Treeview",
                        background="#2E2E2E",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#2E2E2E",
                        bordercolor="#404040",
                        font=("Helvetica", 12))

        # Configure the headings (columns)
        style.configure("Treeview.Heading",
                        background="#1F1F1F",
                        foreground="white",
                        bordercolor="#404040",
                        relief="flat",
                        font=("Helvetica", 14, "bold"))


        style.map("Treeview", background=[("selected", "#565656")])

        style.configure("Treeview", borderwidth=0, relief="flat")
        style.configure("Treeview.Heading", borderwidth=0, relief="flat")

        self.table_event_display = ttk.Treeview(master=self.frame,
                                        columns=("Event Name", "Event Message", "Severity", "Recurring"),
                                        show="headings",
                                        height=20,
                                        style="Treeview")

        self.table_event_display.heading("Event Name", text="Event Name")
        self.table_event_display.heading("Event Message", text="Event Message")
        self.table_event_display.heading("Severity", text="Severity")
        self.table_event_display.heading("Recurring", text="Recurring")

        self.table_event_display.column("Event Name", width=100)
        self.table_event_display.column("Event Message", width=200)
        self.table_event_display.column("Severity", width=50)
        self.table_event_display.column("Recurring", width=50)

        self.table_event_display.grid(row=3, column=3, padx=10, pady=10, sticky="ew", columnspan=8, rowspan=10)


    def add_event(self):
        event_name = self.entry_event_name.get()
        event_message = self.entry_event_message.get()
        event_severity = self.entry_event_severity.get()
        event_reacurring = self.entry_event_reacurring.get()

        # Prepare the data as a list (or tuple)
        new_event = [event_name, event_message, event_severity, event_reacurring]

        self.table_event_display.insert("", "end", values=new_event)



    def temp(self):
        pass

def main():
    """Main function to start the UI."""
    app = APP()
    app.mainloop()


if __name__ == "__main__":
    # Needed for the exe to work or else the multiprocessing will start multiple instances of the app.
    multiprocessing.freeze_support()
    logger = setup_logger(__name__)
    logger.info("Started the program")
    main()