import pygame

class Presentation:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Règles du Tetris")

        # Dimensions
        self.width = 800
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Couleurs
        self.bg_color = (10, 10, 30)
        self.text_color = (255, 255, 255)
        self.highlight_color = (90, 60, 150)

        # Polices
        self.title_font = pygame.font.SysFont("arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("arial", 22)
        self.button_font = pygame.font.SysFont("arial", 28, bold=True)

        # Bouton retour
        self.button_text = self.button_font.render("Retour", True, (255, 255, 255))
        self.button_rect = self.button_text.get_rect(center=(self.width // 2, self.height - 60))

        # Contenu des règles
        self.rules = [
            "Bienvenue dans Tetris !",
            "",
            " Objectif :",
            "Empilez les pièces pour former des lignes complètes.",
            "Chaque ligne complète disparaît et rapporte des points.",
            "",
            " Commandes :",
            "← →  : Déplacer la pièce",
            "↓     : Descendre plus vite",
            "↑     : Tourner la pièce",
            "ÉCH  : Pause / Menu",
            "",
            " Modes de jeu :",
            "• Tetris Normal : jeu classique",
            "• Tetris Inversé : la gravité est inversée !",
            "• Tetris Fou : l’écran peut se retourner aléatoirement",
            "",
            "Essayez de faire le meilleur score possible !",
        ]

    def draw_rules(self, hover=False):
        self.screen.fill(self.bg_color)

        # Titre
        title = self.title_font.render("RÈGLES DU JEU", True, self.highlight_color)
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)

        # Affichage des règles
        y = 130
        for line in self.rules:
            text = self.text_font.render(line, True, self.text_color)
            rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, rect)
            y += 28

        # Bouton retour 
        button_color = (120, 120, 120) if hover else (100, 100, 100)
        pygame.draw.rect(self.screen, button_color, self.button_rect.inflate(40, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), self.button_rect.inflate(40, 20), 2)
        self.screen.blit(self.button_text, self.button_rect)

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            hover = self.button_rect.inflate(40, 20).collidepoint(mouse_pos)

            self.draw_rules(hover)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if hover:  # clic sur le bouton “Retour”
                        running = False  # revient au menu

            self.clock.tick(60)

        return  
