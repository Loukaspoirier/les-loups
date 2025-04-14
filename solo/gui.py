import tkinter as tk
from tkinter import messagebox
from game import Game


class GameGUI:
    CELL_SIZE = 60

    def __init__(self, master):
        self.master = master
        self.master.title("Les Loups - Solo")
        self.game = None
        self.current_turn = 0
        self.timer = 10
        self.timer_id = None

        self.setup_start_menu()

    def setup_start_menu(self):
        self.config_frame = tk.Frame(self.master)
        self.config_frame.pack()

        tk.Label(self.config_frame, text="Choisissez votre rôle :").grid(row=0, column=0, columnspan=2)
        self.role_var = tk.StringVar(value="wolf")
        tk.Radiobutton(self.config_frame, text="🐺 Loup", variable=self.role_var, value="wolf").grid(row=1, column=0)
        tk.Radiobutton(self.config_frame, text="🧑 Villageois", variable=self.role_var, value="villager").grid(row=1, column=1)

        tk.Label(self.config_frame, text="Lignes :").grid(row=2, column=0)
        self.rows_entry = tk.Entry(self.config_frame)
        self.rows_entry.insert(0, "5")
        self.rows_entry.grid(row=2, column=1)

        tk.Label(self.config_frame, text="Colonnes :").grid(row=3, column=0)
        self.cols_entry = tk.Entry(self.config_frame)
        self.cols_entry.insert(0, "5")
        self.cols_entry.grid(row=3, column=1)

        tk.Label(self.config_frame, text="Tours max :").grid(row=4, column=0)
        self.max_turns_entry = tk.Entry(self.config_frame)
        self.max_turns_entry.insert(0, "10")
        self.max_turns_entry.grid(row=4, column=1)

        tk.Label(self.config_frame, text="Temps par tour (sec) :").grid(row=5, column=0)
        self.turn_time_entry = tk.Entry(self.config_frame)
        self.turn_time_entry.insert(0, "10")
        self.turn_time_entry.grid(row=5, column=1)

        tk.Label(self.config_frame, text="Nombre d'obstacles :").grid(row=6, column=0)
        self.obstacles_entry = tk.Entry(self.config_frame)
        self.obstacles_entry.insert(0, "5")
        self.obstacles_entry.grid(row=6, column=1)

        tk.Button(self.config_frame, text="Lancer la partie", command=self.start_game).grid(row=7, column=0, columnspan=2, pady=10)

    def start_game(self):
        role = self.role_var.get()
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            max_turns = int(self.max_turns_entry.get())
            turn_time = int(self.turn_time_entry.get())
            nb_obstacles = int(self.obstacles_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Merci d’entrer des valeurs valides.")
            return

        self.config_frame.destroy()
        self.game = Game(
            role,
            rows=rows,
            cols=cols,
            max_turns=max_turns,
            turn_time=turn_time,
            nb_obstacles=nb_obstacles
        )
        self.build_interface()
        self.start_turn_timer()

    def build_interface(self):
        self.canvas = tk.Canvas(self.master,
                                width=self.game.cols * self.CELL_SIZE,
                                height=self.game.rows * self.CELL_SIZE)
        self.canvas.pack()

        self.status = tk.Label(self.master, text="")
        self.status.pack()

        self.master.bind("<Up>", lambda event: self.play_turn("up"))
        self.master.bind("<Down>", lambda event: self.play_turn("down"))
        self.master.bind("<Left>", lambda event: self.play_turn("left"))
        self.master.bind("<Right>", lambda event: self.play_turn("right"))

        tk.Label(self.master, text="Utilisez les flèches du clavier pour jouer.").pack(pady=5)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.game.rows):
            for j in range(self.game.cols):
                x0 = j * self.CELL_SIZE
                y0 = i * self.CELL_SIZE
                x1 = x0 + self.CELL_SIZE
                y1 = y0 + self.CELL_SIZE

                pos = (i, j)
                if pos == self.game.player.position:
                    emoji = "🧍"
                elif pos == self.game.pnj.position:
                    emoji = "🐺" if self.game.pnj.role == "wolf" else "🧑"
                elif pos in self.game.board.obstacles:
                    emoji = "⛰️"
                else:
                    emoji = "⬜"

                self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=emoji, font=("Arial", 24))
                self.canvas.create_rectangle(x0, y0, x1, y1)

        self.status.config(
            text=f"Tour {self.current_turn + 1}/{self.game.max_turns} — Temps restant : {self.timer} sec"
        )

    def play_turn(self, direction):
        if self.current_turn >= self.game.max_turns:
            self.end_game("😴 Partie terminée (nombre de tours max atteint).")
            return

        self.game.player.move(
            direction,
            self.game.rows,
            self.game.cols,
            self.game.board.is_obstacle
        )
        self.current_turn += 1
        self.check_victory()
        self.draw_board()
        self.reset_timer()

    def start_turn_timer(self):
        self.timer = self.game.turn_time
        self.tick()

    def tick(self):
        self.status.config(
            text=f"Tour {self.current_turn + 1}/{self.game.max_turns} — Temps restant : {self.timer} sec"
        )
        if self.timer > 0:
            self.timer -= 1
            self.timer_id = self.master.after(1000, self.tick)
        else:
            self.current_turn += 1
            messagebox.showinfo("Tour perdu", "⏳ Temps écoulé, vous avez perdu ce tour !")
            self.draw_board()
            self.reset_timer()
            self.check_victory()

    def reset_timer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        self.start_turn_timer()

    def check_victory(self):
        if self.game.player.position == self.game.pnj.position:
            if self.game.player.role == "wolf":
                self.end_game("🎉 Le loup a mangé le villageois !")
            else:
                self.end_game("💀 Le villageois s’est fait manger !")
        elif self.current_turn >= self.game.max_turns:
            self.end_game("😴 Partie terminée (nombre de tours max atteints).")

    def end_game(self, message):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        messagebox.showinfo("Fin de la partie", message)
        self.master.destroy()
