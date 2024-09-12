import customtkinter


class SettingsWindow(customtkinter.CTkToplevel):
    """Class for the how-to-use window with the video tutorial."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")  # Adjusted height for a more compact look
        self.resizable(False, False)
        self.title("Settings")
        self.attributes('-topmost', 1)

        self.widget_height = 30
        self.widget_width = 190
        self.font = customtkinter.CTkFont(size=18)

        self.frame = customtkinter.CTkFrame(master=self, bg_color="transparent")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

        self.frame.columnconfigure(0, weight=1)

        # Reducing the number of grid row configurations and setting tighter padding
        self.create_label_and_entry(0, "Endpoint", "ex. opc.tcp://192.168.8.14:4840/opcua/server/")
        self.create_label_and_entry(2, "Server name", "Enter server name")
        self.create_label_and_entry(4, "URI", "Enter URI")


    def create_label_and_entry(self, row, placeholder, helper_text):
        """Helper function to create label and entry pairs."""
        helper_label = customtkinter.CTkLabel(
            master=self.frame,
            text=helper_text,
            font=self.font,
        )
        helper_label.grid(row=row, column=0, padx=5, pady=(10, 0), sticky="w")

        entry = customtkinter.CTkEntry(
            master=self.frame,
            placeholder_text=placeholder,
            width=self.widget_width,
            height=self.widget_height,
            font=self.font
        )
        entry.grid(row=row + 1, column=0, padx=5, pady=(0, 10), sticky="we")

    def temp(self):
        pass
