import pygame
import os
import json

WIDTH, HEIGHT = 1600, 900

class GameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Risiko - Mappa")
        self.clock = pygame.time.Clock()
        self.running = True

        # Carica immagine mappa
        map_path = os.path.join("assets", "map.png")
        self.map_img = pygame.image.load(map_path)
        self.map_img = pygame.transform.scale(self.map_img, (WIDTH, HEIGHT))

        # Percorso e caricamento JSON da assets
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_path, "assets", "map.json")



        with open(json_path) as f:
            self.territories_data = json.load(f)

        # Coordinate approssimative per i territori (da adattare)
        self.territory_positions = {
            "Alaska": (100, 200),
            "Northwest Territory": (180, 220),
            "Alberta": (200, 260),
            "Ontario": (260, 300),
            "Quebec": (320, 280),
            "Greenland": (400, 150),
            "Western United States": (220, 360),
            "Eastern United States": (300, 380),
            "Central America": (250, 440),

            "Venezuela": (350, 500),
            "Peru": (320, 560),
            "Brazil": (400, 570),
            "Argentina": (360, 650),

            "Iceland": (500, 120),
            "Scandinavia": (580, 160),
            "Ukraine": (680, 200),
            "Great Britain": (520, 220),
            "Northern Europe": (620, 230),
            "Western Europe": (580, 280),
            "Southern Europe": (630, 320),

            "North Africa": (600, 400),
            "Egypt": (660, 430),
            "East Africa": (720, 500),
            "Congo": (660, 550),
            "South Africa": (700, 600),
            "Madagascar": (760, 620),

            "Ural": (780, 180),
            "Siberia": (880, 160),
            "Yakutsk": (960, 140),
            "Kamchatka": (1080, 160),
            "Irkutsk": (940, 220),
            "Mongolia": (1020, 240),
            "Japan": (1120, 260),
            "Afghanistan": (740, 260),
            "China": (820, 280),
            "Middle East": (720, 320),
            "India": (780, 340),
            "Siam": (840, 400),

            "Indonesia": (900, 520),
            "New Guinea": (940, 580),
            "Western Australia": (860, 600),
            "Eastern Australia": (920, 620),
        }

    def draw_map(self):
        self.screen.blit(self.map_img, (0, 0))
        self.draw_connections()

    def draw_connections(self):
        line_color = (255, 0, 0)  # rosso
        line_width = 3

        for territory, data in self.territories_data.items():
            if territory not in self.territory_positions:
                continue

            pos1 = self.territory_positions[territory]

            for neighbor in data["neighbors"]:
                if neighbor in self.territory_positions:
                    pos2 = self.territory_positions[neighbor]

                    # Evita doppioni (linea da A a B e B a A)
                    if territory < neighbor:
                        pygame.draw.line(self.screen, line_color, pos1, pos2, line_width)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))  # sfondo bianco
            self.draw_map()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = GameUI()
    game.run()
