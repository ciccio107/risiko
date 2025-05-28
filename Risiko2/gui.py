import pygame
import random
import os

from territory import can_move_troops, move_troops


class Territory:
    def __init__(self, name, owner=None):
        self.name = name
        self.owner = owner
        self.armies = 0
        self.neighbors = []

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class GUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Risiko")
        self.screen = pygame.display.set_mode((1600, 900))
        self.font = pygame.font.SysFont(None, 24)
        self.clock = pygame.time.Clock()

        map_path = os.path.join("assets", "map.png")
        self.map_image = pygame.image.load(map_path)

        self.players = [Player("Giocatore 1", (220, 20, 60)), Player("IA", (30, 144, 255))]
        self.turno = 1  # 1 = giocatore, 2 = IA
        self.current_player = self.players[0]

        # Posizioni territori
        self.territory_positions = {
            "Alaska": (90, 80), "Northwest Territory": (200, 80), "Alberta": (160, 125),
            "Ontario": (255, 130), "Quebec": (330, 130), "Greenland": (470, 40),
            "Western United States": (150, 180), "Eastern United States": (230, 200),
            "Central America": (180, 300), "Venezuela": (280, 350), "Peru": (290, 450),
            "Brazil": (360, 430), "Argentina": (320, 540), "Iceland": (500, 95),
            "Scandinavia": (640, 70), "Ukraine": (730, 120), "Great Britain": (565, 110),
            "Northern Europe": (630, 140), "Western Europe": (570, 160),
            "Southern Europe": (650, 180), "North Africa": (590, 280), "Egypt": (670, 260),
            "East Africa": (720, 330), "Congo": (670, 380), "South Africa": (670, 480),
            "Madagascar": (790, 470), "Ural": (830, 100), "Siberia": (900, 70),
            "Yakutsk": (1020, 70), "Kamchatka": (1150, 80), "Irkutsk": (980, 120),
            "Mongolia": (1000, 170), "Japan": (1150, 190), "Afghanistan": (850, 170),
            "China": (960, 210), "Middle East": (750, 220), "India": (900, 250),
            "Siam": (1030, 300), "Indonesia": (1080, 380), "New Guinea": (1200, 400),
            "Western Australia": (1100, 510), "Eastern Australia": (1180, 480)
        }

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
            "Venezuela": ["Central America", "Brazil", "Peru"], "Peru": ["Venezuela", "Brazil", "Argentina"],
            "Brazil": ["Venezuela", "Peru", "Argentina", "North Africa"], "Argentina": ["Peru", "Brazil"],
            "Iceland": ["Greenland", "Great Britain", "Scandinavia"],
            "Scandinavia": ["Iceland", "Great Britain", "Northern Europe", "Ukraine"],
            "Ukraine": ["Scandinavia", "Northern Europe", "Ural", "Afghanistan", "Middle East", "Southern Europe"],
            "Great Britain": ["Iceland", "Scandinavia", "Northern Europe", "Western Europe"],
            "Northern Europe": ["Great Britain", "Scandinavia", "Ukraine", "Western Europe", "Southern Europe"],
            "Western Europe": ["Great Britain", "Northern Europe", "Southern Europe", "North Africa"],
            "Southern Europe": ["Western Europe", "Northern Europe", "Ukraine", "Middle East", "North Africa", "Egypt"],
            "North Africa": ["Western Europe", "Southern Europe", "Egypt", "Congo", "Brazil", "East Africa"],
            "Egypt": ["North Africa", "Southern Europe", "Middle East", "East Africa"],
            "East Africa": ["Egypt", "Middle East", "Congo", "South Africa", "Madagascar", "North Africa"],
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
            "Eastern Australia": ["Western Australia", "New Guinea"]
        }

        self.territories = {name: Territory(name) for name in self.territory_positions}
        for t_name, neighbors in neighbors_data.items():
            self.territories[t_name].neighbors = neighbors

        self.territories_list = list(self.territories.values())
        self.distribute_armies_randomly()

        self.attack_from = None
        self.attack_to = None
        self.move_from = None
        self.move_to = None

        # Bottone passa turno (posizione e dimensioni)
        self.pass_button_rect = pygame.Rect(1400, 820, 150, 50)

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

    def can_move_troops(self, from_territory, to_territory):
        return (
                from_territory.owner == self.current_player and
                to_territory.owner == self.current_player and
                to_territory.name in from_territory.neighbors and
                from_territory.armies > 1
        )

    def move_troops(self, from_territory, to_territory, num):
        if num < 1 or from_territory.armies <= num:
            return False
        from_territory.armies -= num
        to_territory.armies += num
        return True

    def handle_middle_click(self, pos):
        clicked_territory = self.get_territory_at_pos(pos)
        if clicked_territory:
            if self.move_from is None:
                if clicked_territory.owner == self.current_player and clicked_territory.armies > 1:
                    self.move_from = clicked_territory
                    print(f"Selezionato da spostare: {clicked_territory.name}")
                else:
                    print("Non puoi spostare truppe da qui.")
            else:
                self.move_to = clicked_territory
                if self.can_move_troops(self.move_from, self.move_to):
                    try:
                        num = int(
                            input(f"Quante truppe vuoi spostare da {self.move_from.name} a {self.move_to.name}? "))
                        if self.move_troops(self.move_from, self.move_to, num):
                            print(f"{num} truppe spostate.")
                        else:
                            print("Spostamento non valido.")
                    except ValueError:
                        print("Input non valido.")
                else:
                    print("Spostamento non valido.")
                self.move_from = None
                self.move_to = None

    def handle_territory_click(territory, current_player):
        global selected_from, selected_to
        if selected_from is None:
            if territory.owner == current_player and territory.troops > 1:
                selected_from = territory
                print(f"Hai selezionato {territory.name} per spostare truppe.")
        else:
            selected_to = territory
            if selected_to == selected_from:
                print("Territorio selezionato due volte. Annullato.")
                selected_from = None
                selected_to = None
                return

            if can_move_troops(selected_from, selected_to, current_player):
                try:
                    num = int(input(f"Quante truppe vuoi spostare da {selected_from.name} a {selected_to.name}? "))
                    if move_troops(selected_from, selected_to, num):
                        print(f"{num} truppe spostate.")
                    else:
                        print("Numero di truppe non valido.")
                except ValueError:
                    print("Input non valido.")
            else:
                print("Spostamento non permesso.")
            selected_from = None
            selected_to = None



    def handle_left_click(self, pos):
        if self.turno != 1:
            return  # azioni solo turno giocatore

        clicked_territory = self.get_territory_at_pos(pos)
        if clicked_territory:
            if self.attack_from is None:
                if clicked_territory.owner == self.current_player and clicked_territory.armies > 1:
                    self.attack_from = clicked_territory
            elif self.attack_to is None:
                if clicked_territory.name in self.attack_from.neighbors and clicked_territory.owner != self.current_player:
                    self.attack_to = clicked_territory
                    self.resolve_attack()
                    self.attack_from = None
                    self.attack_to = None

    def resolve_attack(self):
        # Semplice risoluzione dell'attacco
        if not self.attack_from or not self.attack_to:
            return

        attaccante = self.attack_from
        difensore = self.attack_to

        attacco_armies = min(attaccante.armies - 1, 3)
        difesa_armies = min(difensore.armies, 2)

        attacco_dadi = sorted([random.randint(1, 6) for _ in range(attacco_armies)], reverse=True)
        difesa_dadi = sorted([random.randint(1, 6) for _ in range(difesa_armies)], reverse=True)

        for a_die, d_die in zip(attacco_dadi, difesa_dadi):
            if a_die > d_die:
                difensore.armies -= 1
            else:
                attaccante.armies -= 1

        if difensore.armies <= 0:
            difensore.owner = attaccante.owner
            difensore.armies = attacco_armies
            attaccante.armies -= attacco_armies

    def pass_turn(self):
        if self.turno == 1:
            print("Turno giocatore finito, turno IA")
            self.turno = 2
            self.current_player = self.players[1]
            self.attack_from = None
            self.attack_to = None
            self.ia_turn()
        else:
            print("Turno IA finito, turno giocatore")
            self.turno = 1
            self.current_player = self.players[0]
            self.attack_from = None
            self.attack_to = None

    def ia_turn(self):
        # Cerca un attacco da fare
        ia_territories = [t for t in self.territories_list if t.owner == self.current_player and t.armies > 1]

        for t in ia_territories:
            for neighbor_name in t.neighbors:
                neighbor = self.territories[neighbor_name]
                if neighbor.owner != self.current_player:
                    self.attack_from = t
                    self.attack_to = neighbor
                    self.resolve_attack()
                    # Passa turno dopo il primo attacco IA
                    self.pass_turn()
                    return

        # Se nessun attacco possibile, passa subito turno
        self.pass_turn()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.map_image, (0, 0))

        for territory in self.territories_list:
            x, y = self.territory_positions[territory.name]
            pygame.draw.circle(self.screen, territory.owner.color, (x, y), 15)
            txt = self.font.render(str(territory.armies), True, (255, 255, 255))
            self.screen.blit(txt, (x - txt.get_width() // 2, y - txt.get_height() // 2))

            # Evidenzia il territorio attaccante o attaccato
            if territory == self.attack_from:
                pygame.draw.circle(self.screen, (255, 255, 0), (x, y), 20, 3)
            if territory == self.attack_to:
                pygame.draw.circle(self.screen, (255, 140, 0), (x, y), 20, 3)

        # Disegna bottone passa turno
        pygame.draw.rect(self.screen, (100, 100, 100), self.pass_button_rect)
        button_text = self.font.render("Passa Turno", True, (255, 255, 255))
        self.screen.blit(button_text, (self.pass_button_rect.x + 20, self.pass_button_rect.y + 15))

        # Mostra a chi è il turno
        turn_text = self.font.render(f"Turno di: {self.current_player.name}", True, (0, 0, 0))
        self.screen.blit(turn_text, (20, 20))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # click sinistro
                        pos = pygame.mouse.get_pos()
                        if self.pass_button_rect.collidepoint(pos):
                            self.pass_turn()
                        else:
                            self.handle_left_click(pos)

                    elif event.button == 2:  # click centrale
                        pos = pygame.mouse.get_pos()
                        self.handle_middle_click(pos)

            self.draw()

        pygame.quit()

if __name__ == "__main__":
    gui = GUI()
    gui.run()