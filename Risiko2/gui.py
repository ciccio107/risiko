import pygame
import random
import  os

class Territory:
    def __init__(self, name, owner=None):
        self.name = name
        self.owner = owner  # giocatore proprietario
        self.armies = 0
        self.neighbors = []

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1600, 900))
        self.font = pygame.font.SysFont(None, 24)
        self.clock = pygame.time.Clock()

        # Carica immagine mappa da assets
        map_path = os.path.join("assets", "map.png")
        self.map_image = pygame.image.load(map_path)

        self.players = [Player("Giocatore 1", (255, 0, 0)), Player("Giocatore 2", (0, 0, 255))]
        self.current_player = self.players[0]

        # Mappa territori e posizioni
        self.territory_positions = {
            "Alaska": (100, 100),
            "Northwest Territory": (260, 110),
            "Alberta": (200, 170),
            "Ontario": (300, 180),
            "Quebec": (430, 170),
            "Greenland": (600, 60),
            "Western United States": (170, 250),
            "Eastern United States": (300, 280),
            "Central America": (180, 380),
            "Venezuela": (340, 480),
            "Peru": (340, 610),
            "Brazil": (460, 580),
            "Argentina": (390, 750),
            "Iceland": (660, 95),
            "Scandinavia": (810, 100),
            "Ukraine": (900, 170),
            "Great Britain": (700, 160),
            "Northern Europe": (780, 190),
            "Western Europe": (735, 220),
            "Southern Europe": (800, 240),
            "North Africa": (750, 400),
            "Egypt": (840, 340),
            "East Africa": (900, 450),
            "Congo": (850, 540),
            "South Africa": (860, 680),
            "Madagascar": (980, 640),
            "Ural": (1050, 130),
            "Siberia": (1150, 120),
            "Yakutsk": (1280, 100),
            "Kamchatka": (1400, 110),
            "Irkutsk": (1250, 170),
            "Mongolia": (1300, 220),
            "Japan": (1435, 285),
            "Afghanistan": (1050, 220),
            "China": (1250, 300),
            "Middle East": (960, 300),
            "India": (1100, 340),
            "Siam": (1270, 400),
            "Indonesia": (1350, 510),
            "New Guinea": (1500, 550),
            "Western Australia": (1370, 700),
            "Eastern Australia": (1480, 680),
        }

        # Crea territori
        self.territories = {}
        for name in self.territory_positions.keys():
            self.territories[name] = Territory(name)

        # Definisci neighbors (confini)
        neighbors_data = {
            "Alaska": ["Northwest Territory", "Alberta", "Kamchatka"],
            "Northwest Territory": ["Alaska", "Alberta", "Ontario", "Greenland"],
            "Alberta": ["Alaska", "Northwest Territory", "Ontario", "Western United States"],
            "Ontario": ["Northwest Territory", "Alberta", "Eastern United States", "Quebec", "Greenland"],
            "Quebec": ["Ontario", "Eastern United States", "Greenland"],
            "Greenland": ["Northwest Territory", "Ontario", "Quebec", "Iceland"],
            "Western United States": ["Alberta", "Ontario", "Eastern United States", "Central America"],
            "Eastern United States": ["Western United States", "Ontario", "Quebec", "Central America"],
            "Central America": ["Western United States", "Eastern United States", "Venezuela"],
            "Venezuela": ["Central America", "Brazil", "Peru"],
            "Peru": ["Venezuela", "Brazil", "Argentina"],
            "Brazil": ["Venezuela", "Peru", "Argentina", "North Africa"],
            "Argentina": ["Peru", "Brazil"],
            "Iceland": ["Greenland", "Great Britain", "Scandinavia"],
            "Scandinavia": ["Iceland", "Great Britain", "Northern Europe", "Ukraine"],
            "Ukraine": ["Scandinavia", "Northern Europe", "Ural", "Afghanistan", "Middle East"],
            "Great Britain": ["Iceland", "Scandinavia", "Northern Europe", "Western Europe"],
            "Northern Europe": ["Great Britain", "Scandinavia", "Ukraine", "Western Europe", "Southern Europe"],
            "Western Europe": ["Great Britain", "Northern Europe", "Southern Europe", "North Africa"],
            "Southern Europe": ["Western Europe", "Northern Europe", "Ukraine", "Middle East", "North Africa", "Egypt"],
            "North Africa": ["Western Europe", "Southern Europe", "Egypt", "Congo", "Brazil"],
            "Egypt": ["North Africa", "Southern Europe", "Middle East", "East Africa"],
            "East Africa": ["Egypt", "Middle East", "Congo", "South Africa", "Madagascar"],
            "Congo": ["North Africa", "East Africa", "South Africa"],
            "South Africa": ["Congo", "East Africa", "Madagascar"],
            "Madagascar": ["South Africa", "East Africa"],
            "Ural": ["Ukraine", "Siberia", "China", "Afghanistan"],
            "Siberia": ["Ural", "Yakutsk", "Irkutsk", "Mongolia", "China"],
            "Yakutsk": ["Siberia", "Kamchatka", "Irkutsk"],
            "Kamchatka": ["Yakutsk", "Irkutsk", "Mongolia", "Japan", "Alaska"],
            "Irkutsk": ["Siberia", "Yakutsk", "Kamchatka", "Mongolia"],
            "Mongolia": ["Siberia", "Irkutsk", "Kamchatka", "Japan", "China"],
            "Japan": ["Kamchatka", "Mongolia"],
            "Afghanistan": ["Ukraine", "Ural", "China", "India", "Middle East"],
            "China": ["Siberia", "Mongolia", "Afghanistan", "India", "Siam"],
            "Middle East": ["Ukraine", "Afghanistan", "India", "Egypt", "East Africa"],
            "India": ["Middle East", "Afghanistan", "China", "Siam"],
            "Siam": ["India", "China", "Indonesia"],
            "Indonesia": ["Siam", "New Guinea", "Western Australia"],
            "New Guinea": ["Indonesia", "Eastern Australia"],
            "Western Australia": ["Indonesia", "Eastern Australia"],
            "Eastern Australia": ["Western Australia", "New Guinea"],
        }

        # Assegna neighbors ai territori
        for t_name, neighbors in neighbors_data.items():
            self.territories[t_name].neighbors = neighbors

        # Convert territories dict to list for iteration
        self.territories_list = list(self.territories.values())

        # Distribuisci truppe e proprietari casuali
        self.distribute_armies_randomly()

        # Variabili attacco
        self.attack_from = None
        self.attack_to = None

    def distribute_armies_randomly(self):
        for territory in self.territories_list:
            territory.owner = random.choice(self.players)
            territory.armies = random.randint(1, 10)

    def get_territory_at_pos(self, pos):
        for territory in self.territories_list:
            x, y = self.territory_positions[territory.name]
            dist = ((pos[0] - x) ** 2 + (pos[1] - y) ** 2) ** 0.5
            if dist < 20:
                return territory
        return None

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.map_image, (0, 0))

        # Disegna confini dei territori
        for territory in self.territories_list:
            x, y = self.territory_positions[territory.name]
            # Cerchio esterno nero
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 20)
            # Cerchio colore proprietario
            pygame.draw.circle(self.screen, territory.owner.color, (x, y), 15)
            # Numero truppe
            text = self.font.render(str(territory.armies), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)

        # Selezioni evidenziate
        if self.attack_from:
            x, y = self.territory_positions[self.attack_from.name]
            pygame.draw.circle(self.screen, (255, 255, 0), (x, y), 25, 3)
        if self.attack_to:
            x, y = self.territory_positions[self.attack_to.name]
            pygame.draw.circle(self.screen, (255, 0, 255), (x, y), 25, 3)

        # Info testo
        info_text = f"Turno: {self.current_player.name} - Clic sinistro: seleziona da attaccare, clic destro: seleziona territorio da attaccare"
        text = self.font.render(info_text, True, (0, 0, 0))
        self.screen.blit(text, (10, 870))

        pygame.display.flip()

    def roll_dice(self, n):
        return sorted([random.randint(1, 6) for _ in range(n)], reverse=True)

    def resolve_attack(self):
        if not self.attack_from or not self.attack_to:
            return

        attacker_armies = self.attack_from.armies
        defender_armies = self.attack_to.armies

        # Numero dadi:
        attacker_dice = min(3, attacker_armies - 1)
        defender_dice = min(2, defender_armies)

        if attacker_dice == 0 or defender_dice == 0:
            print("Non puoi attaccare con così poche truppe")
            return

        attack_rolls = self.roll_dice(attacker_dice)
        defend_rolls = self.roll_dice(defender_dice)

        print(f"{self.attack_from.name} attacca {self.attack_to.name}")
        print(f"Tiri attaccante: {attack_rolls}")
        print(f"Tiri difensore: {defend_rolls}")

        # Confronta i dadi
        for a, d in zip(attack_rolls, defend_rolls):
            if a > d:
                self.attack_to.armies -= 1
                print(f"Il difensore perde 1 truppa, ora ha {self.attack_to.armies}")
            else:
                self.attack_from.armies -= 1
                print(f"L'attaccante perde 1 truppa, ora ha {self.attack_from.armies}")

            # Controllo fine territorio
            if self.attack_to.armies == 0:
                # Conquista territorio
                print(f"{self.current_player.name} conquista {self.attack_to.name}!")
                self.attack_to.owner = self.current_player
                trasferite = attacker_dice  # trasferiamo le truppe che hanno attaccato
                self.attack_from.armies -= trasferite
                self.attack_to.armies = trasferite
                break

        # Reset selezioni
        self.attack_from = None
        self.attack_to = None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # click sinistro
                        self.handle_left_click(event.pos)
                    elif event.button == 3:  # click destro
                        self.handle_right_click(event.pos)

            self.draw()
            self.clock.tick(30)
        pygame.quit()

    def handle_left_click(self, pos):
        clicked_territory = self.get_territory_at_pos(pos)
        if clicked_territory:
            if clicked_territory.owner == self.current_player:
                if clicked_territory.armies > 1:
                    self.attack_from = clicked_territory
                    self.attack_to = None
                    print(f"Selezionato per attaccare da: {clicked_territory.name}")
                else:
                    print("Non puoi attaccare con una sola truppa.")
            else:
                print("Questo territorio non è tuo.")

    def handle_right_click(self, pos):
        if not self.attack_from:
            print("Seleziona prima un territorio da cui attaccare con il click sinistro.")
            return

        clicked_territory = self.get_territory_at_pos(pos)
        if clicked_territory:
            if clicked_territory.name in self.attack_from.neighbors:
                if clicked_territory.owner != self.current_player:
                    self.attack_to = clicked_territory
                    print(f"Selezionato territorio da attaccare: {clicked_territory.name}")
                    self.resolve_attack()
                else:
                    print("Non puoi attaccare un tuo territorio.")
            else:
                print("Il territorio selezionato non confina con quello di partenza.")

if __name__ == "__main__":
    gui = GUI()
    gui.run()
