import tkinter as tk
from tkinter import messagebox
from animation import start_bouncing_hearts, start_pulsing_heart
from puzzle import WordSearchPage

class ValentineApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Valentine's Surprise")
        self.geometry("800x750")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, WordSearchPage, FinalPage):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="white")

        # TOP FRAME: for animations (bouncing hearts + pulsing heart)
        top_frame = tk.Frame(self, bg="white", width=800, height=400)
        top_frame.pack(side="top", fill="both", padx=10, pady=10)
        top_frame.pack_propagate(False)  # Prevent shrinking to contents

        # Create a canvas for the bouncing background hearts.
        self.bg_canvas = tk.Canvas(top_frame, width=800, height=400, bg="white", highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        start_bouncing_hearts(self.bg_canvas)

        # Overlay canvas for the pulsing (beating) big heart.
        self.heart_canvas = tk.Canvas(top_frame, width=300, height=300, bg="white", highlightthickness=0)
        # Place it in the center of the top frame.
        self.heart_canvas.place(relx=0.5, rely=0.5, anchor="center")
        start_pulsing_heart(self.heart_canvas)

        # BOTTOM FRAME: for the question label and Yes/No buttons.
        bottom_frame = tk.Frame(self, bg="white")
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        label = tk.Label(bottom_frame, text="Will you be my Valentine?",
                         font=("Comic Sans MS", 32, "bold"), fg="magenta", bg="white")
        label.pack(pady=10)

        button_frame = tk.Frame(bottom_frame, bg="white")
        button_frame.pack(pady=10)
        yes_button = tk.Button(button_frame, text="Yes", font=("Arial", 16, "bold"),
                               bg="lightgreen", command=lambda: controller.show_frame("WordSearchPage"))
        no_button = tk.Button(button_frame, text="No", font=("Arial", 16, "bold"),
                              bg="tomato", command=self.no_clicked)
        yes_button.pack(side="left", padx=20)
        no_button.pack(side="right", padx=20)

    def no_clicked(self):
        messagebox.showinfo("Oh no!", "Please don't say no! You know you love me :)")

class FinalPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="pink")

        self.canvas = tk.Canvas(self, width=800, height=750, bg="pink", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.bind("<<ShowFrame>>", self.on_show_frame)

    def on_show_frame(self, event):
        self.canvas.delete("all")
        from messages import show_final_message
        show_final_message(self.canvas)

if __name__ == '__main__':
    app = ValentineApp()
    app.mainloop()
