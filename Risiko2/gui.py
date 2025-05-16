import tkinter as tk

class RisikoGUI:
    def __init__(self, master, territori):
        self.master = master
        self.master.title("Risiko - Mappa")
        self.territori = territori

        self.canvas_width = 1200
        self.canvas_height = 800
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.posizioni = {
            # North America
            "Alaska": (80, 80),
            "Northwest Territory": (200, 100),
            "Greenland": (350, 50),
            "Alberta": (180, 200),
            "Ontario": (280, 180),
            "Quebec": (350, 160),
            "Western United States": (190, 320),
            "Eastern United States": (300, 300),
            "Central America": (220, 420),

            # South America
            "Venezuela": (300, 460),
            "Peru": (260, 550),
            "Brazil": (350, 550),
            "Argentina": (300, 650),

            # Europe
            "Iceland": (450, 120),
            "Scandinavia": (570, 130),
            "Ukraine": (700, 230),
            "Great Britain": (470, 220),
            "Northern Europe": (620, 240),
            "Western Europe": (570, 320),
            "Southern Europe": (660, 330),

            # Africa
            "North Africa": (620, 430),
            "Egypt": (730, 430),
            "East Africa": (780, 510),
            "Congo": (640, 600),
            "South Africa": (690, 700),
            "Madagascar": (780, 720),

            # Asia (spostati e distanziati)
            "Ural": (780, 180),
            "Siberia": (870, 130),
            "Yakutsk": (980, 110),
            "Kamchatka": (1100, 110),
            "Irkutsk": (890, 230),
            "Mongolia": (950, 240),
            "Japan": (1030, 240),
            "Afghanistan": (720, 320),
            "China": (830, 320),
            "Middle East": (680, 380),
            "India": (770, 390),
            "Siam": (850, 450),

            # Australia / Oceania (più distanziata)
            "Indonesia": (880, 610),
            "New Guinea": (950, 650),
            "Western Australia": (880, 700),
            "Eastern Australia": (950, 740),
        }

        # Linee speciali che attraversano il bordo del canvas (wrap-around)
        self.linee_speciali = {
            ("Alaska", "Kamchatka"): [(-50, 80), (1250, 110)],
            ("Kamchatka", "Alaska"): [(1250, 110), (-50, 80)],
        }

        self.raggio_territorio = 25
        self.font_nome = ("Arial", 12, "bold")
        self.font_truppe = ("Arial", 14, "bold")

        self.disegna_mappa()

    def disegna_mappa(self):
        self.canvas.delete("all")

        # Disegna linee (normali o wrap-around)
        for territorio in self.territori.values():
            x1, y1 = self.posizioni.get(territorio.name, (0, 0))
            for vicino in territorio.neighbors:
                x2, y2 = self.posizioni.get(vicino, (0, 0))
                if x1 and x2:
                    key = (territorio.name, vicino)
                    if key in self.linee_speciali:
                        punti = self.linee_speciali[key]
                        self.canvas.create_line(x1, y1, punti[0][0], punti[0][1], fill="gray", width=2)
                        self.canvas.create_line(punti[1][0], punti[1][1], x2, y2, fill="gray", width=2)
                    else:
                        self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)

        # Disegna territori come cerchi con testo
        for territorio in self.territori.values():
            x, y = self.posizioni.get(territorio.name, (0, 0))
            if x == 0 and y == 0:
                continue

            if territorio.owner:
                colore = "red" if territorio.owner.name == "Giocatore 1" else "blue"
            else:
                colore = "gray"

            r = self.raggio_territorio
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=colore, outline="black", width=2)
            self.canvas.create_text(x, y - r - 10, text=territorio.name, font=self.font_nome, fill="black")
            self.canvas.create_text(x, y, text=str(territorio.troops), font=self.font_truppe, fill="white")

def avvia_gui(territori):
    root = tk.Tk()
    app = RisikoGUI(root, territori)
    root.mainloop()
