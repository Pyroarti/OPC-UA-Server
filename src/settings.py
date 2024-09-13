import pathlib
import json

import customtkinter
from CTkMessagebox import CTkMessagebox

from create_logger import setup_logger


class SettingsWindow(customtkinter.CTkToplevel):
    """Setting to create a server"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        parent.update_idletasks()  # Ensure the parent window is updated with its size
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        self.update_idletasks()  # Ensure the toplevel window is updated with its size
        toplevel_width = self.winfo_width()
        toplevel_height = self.winfo_height()

        # Calculate the position to center the toplevel window relative to the parent
        center_x = parent_x + (parent_width // 2) - (toplevel_width // 2)
        center_y = parent_y + (parent_height // 2) - (toplevel_height // 2)

        self.geometry(f"{500}x{400}+{center_x}+{center_y}")
        self.resizable(False, False)
        self.title("Settings")
        self.attributes('-topmost', 1)

        self.logger = setup_logger(__name__)

        self.widget_height = 30
        self.widget_width = 190
        self.font = customtkinter.CTkFont(size=18)

        self.frame = customtkinter.CTkFrame(master=self, bg_color="transparent")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

        self.frame.columnconfigure(0, weight=1)

        # Endpoint Label and Entry
        self.endpoint_label = customtkinter.CTkLabel(
            master=self.frame,
            text="ex. opc.tcp://192.168.8.14:4840/opcua/server/",
            font=self.font
        )
        self.endpoint_label.grid(row=0, column=0, padx=5, pady=(10, 0), sticky="w")

        self.endpoint_entry = customtkinter.CTkEntry(
            master=self.frame,
            placeholder_text="Endpoint",
            width=self.widget_width,
            height=self.widget_height,
            font=self.font
        )
        self.endpoint_entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="we")

        # Server Name Label and Entry
        self.server_name_label = customtkinter.CTkLabel(
            master=self.frame,
            text="Enter server name",
            font=self.font
        )
        self.server_name_label.grid(row=2, column=0, padx=5, pady=(10, 0), sticky="w")

        self.server_name_entry = customtkinter.CTkEntry(
            master=self.frame,
            placeholder_text="Server name",
            width=self.widget_width,
            height=self.widget_height,
            font=self.font
        )
        self.server_name_entry.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="we")

        # Save Button
        self.save_button = customtkinter.CTkButton(
            master=self.frame,
            text="Save",
            font=self.font,
            command=self.save_setting
        )
        self.save_button.grid(row=6, column=0, padx=5, pady=(10, 0), sticky="we")

    def save_setting(self):
        # Get the values from the entries
        endpoint = self.endpoint_entry.get()
        server_name = self.server_name_entry.get()
        if not server_name or not endpoint:
            return CTkMessagebox(title="Error", message="Please fill all the fields", icon="cancel")

        # Prepare the settings data
        settings_data = {
            "server_endpoint": endpoint,
            "server_name": server_name,
        }

        # Save the settings to a JSON file
        parent = pathlib.Path(__file__).parent.parent
        server_file = parent / "server.json"

        try:
            with open(server_file, 'w') as file:
                json.dump(settings_data, file, indent=4)
                self.logger.info("Settings saved successfully")
                self.destroy()
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            return CTkMessagebox(title="Error", message= e, icon="cancel")

