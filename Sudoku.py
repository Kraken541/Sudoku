import tkinter as tk
from tkinter import messagebox
import random

class SudokuGame:
    def __init__(self, root, board):
        self.root = root
        self.root.title("Sudoku Game")
        self.board = board
        self.size = len(board)
        self.block_size = int(self.size**0.5)
        self.cells = {}
        self.lives = 5

        self.create_widgets()

    def create_widgets(self):
        for i in range(self.size):
            for j in range(self.size):
                cell_frame = tk.Frame(
                    self.root,
                    highlightbackground="black",
                    highlightcolor="black",
                    highlightthickness=1,
                    width=50,
                    height=50,
                    padx=3,
                    pady=3
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                entry = tk.Entry(cell_frame, width=2, font=('Arial', 24), justify='center')
                entry.grid(row=0, column=0)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(state='readonly')
                entry.bind('<FocusOut>', lambda event, row=i, col=j: self.validate_entry(event, row, col))
                self.cells[(i, j)] = entry

        new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        new_game_button.grid(row=self.size, column=0, columnspan=self.size, pady=10)

        self.lives_label = tk.Label(self.root, text=f"Lives: {self.lives}", font=('Arial', 16))
        self.lives_label.grid(row=self.size + 1, column=0, columnspan=self.size, pady=10)

    def validate_entry(self, event, row, col):
        entry = event.widget
        try:
            num = int(entry.get())
            if num < 1 or num > self.size or not self.is_valid(row, col, num):
                self.lives -= 1
                self.lives_label.config(text=f"Lives: {self.lives}")
                if self.lives <= 0:
                    messagebox.showinfo("Game Over", "You have run out of lives. Game Over!")
                    self.root.quit()
                else:
                    messagebox.showerror("Invalid Move", "The number is not valid for this position.")
                entry.delete(0, tk.END)
            else:
                self.board[row][col] = num
                if self.is_solved():
                    self.show_win_screen()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            entry.delete(0, tk.END)

    def is_valid(self, row, col, num):
        # Проверка строки
        if num in self.board[row]:
            return False

        # Проверка столбца
        if num in [self.board[i][col] for i in range(self.size)]:
            return False

        # Проверка блока
        start_row, start_col = self.block_size * (row // self.block_size), self.block_size * (col // self.block_size)
        for i in range(start_row, start_row + self.block_size):
            for j in range(start_col, start_col + self.block_size):
                if self.board[i][j] == num:
                    return False

        return True

    def is_solved(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return False
        return True

    def show_win_screen(self):
        win_screen = tk.Toplevel(self.root)
        win_screen.title("You Win!")
        win_screen.geometry("300x200")
        win_label = tk.Label(win_screen, text="You Win!", font=('Arial', 24))
        win_label.pack(pady=50)
        win_screen.transient(self.root)
        win_screen.grab_set()
        self.root.wait_window(win_screen)

    def new_game(self):
        self.board = generate_sudoku()
        self.lives = 5
        self.lives_label.config(text=f"Lives: {self.lives}")
        for (i, j), entry in self.cells.items():
            entry.config(state='normal')
            entry.delete(0, tk.END)
            if self.board[i][j] != 0:
                entry.insert(0, str(self.board[i][j]))
                entry.config(state='readonly')
            else:
                entry.config(state='normal')

def generate_sudoku():
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        return random.sample(s, len(s))

    r_base = range(base)
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
    nums = shuffle(range(1, base * base + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = side * side
    empties = squares * 3 // 4
    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board

def main():
    root = tk.Tk()
    board = generate_sudoku()
    game = SudokuGame(root, board)
    root.mainloop()

if __name__ == "__main__":
    main()
