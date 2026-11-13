import customtkinter as ctk

ctk.set_appearance_mode("dark")

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Trash-Autonomous | Dashboard by MILKAA ")
        self.geometry("920x720")
        self.minsize(480, 360)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Trash-Autonomous Dashboard",
            justify="center",
            font=("Open Sans", 35, "bold")
        )
        self.title_label.grid(row=1, column=0, pady=20, sticky="ew")
        self.v = ctk.CTkLabel(
            self,
            text = "Version: 1.1"

        )
        self.v.grid(row=5, column=0, pady=15, sticky="ew")
        
        self.status = ctk.CTkLabel(
            self, 
            text="", 
            font=("Open Sans", 18)
        )
        self.status.grid(row=2, column=0, pady=20)

        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=3, column=0, pady=10)

        def blank():
            print("Ahh")


        self.blank = ctk.CTkButton(
            self.buttons_frame,
            text="Make blank Trash-Autonomous",
            fg_color="Red",
            cursor="hand2",
            hover_color="#e41e1e",
            command=blank
        )
        self.blank.grid(row=0, column=1, padx=8)
        self.appearing()


    def appearing(self):
        def start():
            print("start!")

        self.status.configure(text="Connect your PC to the 2nd port of the ESP32")
        self.btn = ctk.CTkButton(self.buttons_frame, text="Upload the code", fg_color="Orange", cursor='hand2', hover_color="#ebc040", command=start)
        self.btn.grid(row=0, column=0, padx=8)


if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()