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
            "Alaska": (100, 100),# coordinate giuste
            "Northwest Territory": (260, 110),#
            "Alberta": (200, 170),#
            "Ontario": (300, 180),#
            "Quebec": (430, 170),#
            "Greenland": (600, 60),#
            "Western United States": (170, 250),#
            "Eastern United States": (300, 280),#
            "Central America": (180, 380),#

            "Venezuela": (340, 480),#
            "Peru": (340, 610),#
            "Brazil": (460, 580),#
            "Argentina": (390, 750),#

            "Iceland": (500, 120),
            "Scandinavia": (580, 160),
            "Ukraine": (680, 200),
            "Great Britain": (520, 220),
            "Northern Europe": (620, 230),
            "Western Europe": (580, 280),
            "Southern Europe": (630, 320),

            "North Africa": (750, 400),#
            "Egypt": (840, 340),#
            "East Africa": (900, 450),#
            "Congo": (850, 540),#
            "South Africa": (860, 680),#
            "Madagascar": (980, 640), #

            "Ural": (780, 180),
            "Siberia": (880, 160),
            "Yakutsk": (1280, 100),#
            "Kamchatka": (1400, 110),#
            "Irkutsk": (940, 220),
            "Mongolia": (1300, 220),#
            "Japan": (1435, 285),#
            "Afghanistan": (1050, 220),
            "China": (1250, 300),#
            "Middle East": (960, 300),#
            "India": (1100, 340),
            "Siam": (1270, 400),#

            "Indonesia": (1350, 510),#
            "New Guinea": (1500, 550),#
            "Western Australia": (1370, 700),#
            "Eastern Australia": (1480, 680),#
        }

    def draw_map(self):
        self.screen.blit(self.map_img, (0, 0))
        self.draw_connections()

    def draw_connections(self):
        line_color = (0, 0, 0)  # rosso
        line_width = 5

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
