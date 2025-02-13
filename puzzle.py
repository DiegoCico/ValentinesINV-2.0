import tkinter as tk
from tkinter import messagebox
import random
import string

class WordSearchPage(tk.Frame):
    """
    Interactive word search puzzle page.
    """
    def __init__(self, parent, controller):
        """
        Initializes the WordSearchPage with title, status counters, hint button,
        grid canvas, and back button.
        
        :param parent: The parent widget.
        :param controller: The main application controller.
        """
        super().__init__(parent)
        self.controller = controller
        self.config(bg="lightyellow")
        top_frame = tk.Frame(self, bg="lightyellow")
        top_frame.pack(side="top", fill="x")
        title = tk.Label(top_frame, text="Find the Hidden Words!", font=("Helvetica", 24, "bold"), bg="lightyellow", fg="darkblue")
        title.pack(pady=10)
        self.words = ["LOVE", "GABITA", "HAPPY", "VALENTINES", "SHABOINKING"]
        self.found_label = tk.Label(top_frame, text="Words found: 0", font=("Helvetica", 16), bg="lightyellow", fg="black")
        self.found_label.pack(pady=5)
        self.remaining_label = tk.Label(top_frame, text="Words left: " + str(len(self.words)), font=("Helvetica", 16), bg="lightyellow", fg="black")
        self.remaining_label.pack(pady=5)
        instructions = tk.Label(top_frame, text="Search for the words", font=("Helvetica", 16), bg="lightyellow", fg="black")
        instructions.pack(pady=5)
        self.hint_button = tk.Button(top_frame, text="Hint", font=("Helvetica", 12), command=self.show_hint)
        self.hint_button.place(relx=0.95, rely=0.05, anchor="ne")
        canvas_frame = tk.Frame(self, bg="lightyellow")
        canvas_frame.pack(side="top", fill="both", expand=True)
        self.rows = 12
        self.cols = 12
        self.cell_size = 40
        self.letter_grid, self.placements = self.generate_word_search(self.rows, self.cols, self.words)
        print("Generated Word Search Grid:")
        for row in self.letter_grid:
            print(" ".join(row))
        self.found_words = {}
        self.canvas = tk.Canvas(canvas_frame, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg="white")
        self.canvas.pack(pady=10)
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        back_button = tk.Button(self, text="Back", font=("Helvetica", 12), command=lambda: controller.show_frame("HomePage"))
        back_button.pack(pady=5)
        self.start_cell = None
        self.temp_line = None

    def show_hint(self):
        """
        Displays a hint for one randomly selected word from those not yet found.
        """
        remaining = [word for word in self.words if word not in self.found_words]
        if not remaining:
            messagebox.showinfo("Hint", "All words found!")
            return
        chosen = random.choice(remaining)
        hint_mapping = {"HAPPY": "HOLIDAY", "VALENTINES": "HOLIDAY", "GABITA": "NICKNAME", "LOVE": "WHAT WE DO WITH IN A BED", "SHABOINKING" : "Fun time ;)"}
        hint_text = hint_mapping.get(chosen, "No hint available")
        messagebox.showinfo("Hint", f"Hint: {hint_text}")

    def generate_word_search(self, rows, cols, words):
        """
        Generates a word search grid with the specified words.
        
        :param rows: Number of rows in the grid.
        :param cols: Number of columns in the grid.
        :param words: List of words to hide in the grid.
        :return: Tuple (letter_grid, placements) where letter_grid is the completed grid and placements maps words to their placements.
        """
        grid = [[None for _ in range(cols)] for _ in range(rows)]
        placements = {}
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for word in words:
            valid_placements = []
            length = len(word)
            for dr, dc in directions:
                for row in range(rows):
                    for col in range(cols):
                        end_row = row + dr * (length - 1)
                        end_col = col + dc * (length - 1)
                        if not (0 <= end_row < rows and 0 <= end_col < cols):
                            continue
                        can_place = True
                        r, c = row, col
                        for letter in word:
                            if grid[r][c] is not None and grid[r][c] != letter:
                                can_place = False
                                break
                            r += dr
                            c += dc
                        if can_place:
                            valid_placements.append((row, col, end_row, end_col, dr, dc))
            if valid_placements:
                chosen = random.choice(valid_placements)
                start_row, start_col, end_row, end_col, dr, dc = chosen
                r, c = start_row, start_col
                for letter in word:
                    grid[r][c] = letter
                    r += dr
                    c += dc
                placements[word] = (start_row, start_col, end_row, end_col)
            else:
                print(f"Could not place the word: {word}")
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] is None:
                    grid[r][c] = random.choice(string.ascii_uppercase)
        return grid, placements

    def draw_grid(self):
        """
        Draws the word search grid and any permanent highlights for found words on the canvas.
        """
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")
                self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=self.letter_grid[r][c], font=("Helvetica", 16), fill="black", tags="letter")
        for word, coords in self.found_words.items():
            self.highlight_word(coords)
        self.canvas.tag_raise("letter")

    def on_mouse_down(self, event):
        """
        Records the starting cell of the selection when the mouse button is pressed.
        """
        row = event.y // self.cell_size
        col = event.x // self.cell_size
        self.start_cell = (row, col)
        if self.temp_line is not None:
            self.canvas.delete(self.temp_line)
            self.temp_line = None

    def on_mouse_move(self, event):
        """
        Updates the temporary selection line while the mouse is dragged.
        """
        if self.start_cell is None:
            return
        start_row, start_col = self.start_cell
        x_start = start_col * self.cell_size + self.cell_size/2
        y_start = start_row * self.cell_size + self.cell_size/2
        if self.temp_line is None:
            self.temp_line = self.canvas.create_line(x_start, y_start, event.x, event.y, fill="blue", width=3)
        else:
            self.canvas.coords(self.temp_line, x_start, y_start, event.x, event.y)

    def on_mouse_up(self, event):
        """
        Finalizes the selection when the mouse button is released and checks if it matches any hidden word.
        """
        if self.start_cell is None:
            return
        end_x = min(max(event.x, 0), self.cols * self.cell_size - 1)
        end_y = min(max(event.y, 0), self.rows * self.cell_size - 1)
        end_row = end_y // self.cell_size
        end_col = end_x // self.cell_size
        start_row, start_col = self.start_cell
        dr = end_row - start_row
        dc = end_col - start_col
        step_r = dr // abs(dr) if dr != 0 else 0
        step_c = dc // abs(dc) if dc != 0 else 0
        allowed = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
        if (step_r, step_c) not in allowed:
            self.start_cell = None
            if self.temp_line is not None:
                self.canvas.delete(self.temp_line)
                self.temp_line = None
            return
        if step_r != 0 and step_c != 0 and abs(dr) != abs(dc):
            self.start_cell = None
            if self.temp_line is not None:
                self.canvas.delete(self.temp_line)
                self.temp_line = None
            return
        num_steps = max(abs(dr), abs(dc))
        cells = [(start_row + i * step_r, start_col + i * step_c) for i in range(num_steps + 1)]
        if self.temp_line is not None:
            self.canvas.delete(self.temp_line)
            self.temp_line = None
        for word, placement in self.placements.items():
            pr1, pc1, pr2, pc2 = placement
            for pos in [(pr1, pc1, pr2, pc2), (pr2, pc2, pr1, pc1)]:
                r1, c1, r2, c2 = pos
                expected = []
                length = len(word)
                if length == 1:
                    expected = [(r1, c1)]
                else:
                    s_r = (r2 - r1) // (length - 1) if (r2 - r1) != 0 else 0
                    s_c = (c2 - c1) // (length - 1) if (c2 - c1) != 0 else 0
                    expected = [(r1 + i * s_r, c1 + i * s_c) for i in range(length)]
                if cells == expected:
                    if word not in self.found_words:
                        self.found_words[word] = (r1, c1, r2, c2)
                        self.highlight_word((r1, c1, r2, c2))
                        self.update_status()
                        if len(self.found_words) == len(self.words):
                            messagebox.showinfo("Success", "VALENTINES APPROVED PASSED TEST")
                            self.controller.show_frame("FinalPage")
                    self.start_cell = None
                    return
        self.start_cell = None

    def highlight_word(self, placement):
        """
        Highlights the found word by drawing a full-cell yellow rectangle for each cell in the word.
        
        :param placement: Tuple (r1, c1, r2, c2) specifying the start and end cells.
        """
        r1, c1, r2, c2 = placement
        cells = []
        if r1 == r2:
            for col in range(min(c1, c2), max(c1, c2) + 1):
                cells.append((r1, col))
        elif c1 == c2:
            for row in range(min(r1, r2), max(r1, r2) + 1):
                cells.append((row, c1))
        else:
            length = abs(r2 - r1) + 1
            step_r = (r2 - r1) // (length - 1)
            step_c = (c2 - c1) // (length - 1)
            for i in range(length):
                cells.append((r1 + i * step_r, c1 + i * step_c))
        for row, col in cells:
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", stipple="gray25", outline="", tags="highlight")
        self.canvas.tag_lower("highlight")

    def update_status(self):
        """
        Updates the status labels for found words and remaining words, showing only counters.
        """
        found_count = len(self.found_words)
        remaining_count = len(self.words) - found_count
        self.found_label.config(text="Words found: " + str(found_count))
        self.remaining_label.config(text="Words left: " + str(remaining_count))

    def redraw(self):
        """
        Redraws the word search grid.
        """
        self.draw_grid()

    def event_generate(self, event):
        """
        Triggers a redraw of the canvas.
        """
        self.redraw()
