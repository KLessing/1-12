import pygame
import button
import dice
import draw_only_dice
import score
import random
# import only public functions from module
from validator import *

class Game():
    def __init__(self, screen_size: tuple(), player_names: [str], caption: str, test_modus = False):
        # global init (needed for fonts etc.)
        pygame.init()
        # set game name
        pygame.display.set_caption(caption)

        self.screen_size = screen_size
        self.player_names = player_names
        self.test_modus = test_modus

        #create display window
        self.screen = pygame.display.set_mode(self.screen_size)

        # init background image
        self.background = pygame.image.load('img/table_top.png').convert_alpha()

        # init button images
        confirm_btn_enabled_img = pygame.image.load('img/button_confirm.png').convert_alpha()
        confirm_btn_disabled_img = pygame.image.load('img/button_confirm_disabled.png').convert_alpha()
        finish_btn_img = pygame.image.load('img/button_finish.png').convert_alpha()

        # init global button instances
        self.confirm_btn = button.Button(confirm_btn_enabled_img, 0.8, "confirm", self.screen_size, confirm_btn_disabled_img)
        self.finish_btn = button.Button(finish_btn_img, 0.8, "finish", self.screen_size)

        # init scores for all players
        self.scores = []
        for player_name in player_names:
            self.scores.append(score.Score(player_name, self.screen_size[0]))

        # init dice images
        self.dice_img = {}
        self.selected_dice_img = {}
        for i in range(1, 7):
            self.dice_img[i] = pygame.image.load('img/' + str(i) + '.png').convert_alpha()
            self.selected_dice_img[i] = pygame.image.load('img/' + str(i) + '_selected.png').convert_alpha()
        
        self.current_dice = []
        self.used_dice = []
        self.current_player_index = 0

        # start first move
        self.move()

    def use_test_values(self, count: int):
        test_values = [6, 1, 4, 3, 5, 2]
        for i in range(0, count):
            val = test_values[i]
            self.current_dice.append(dice.Dice(self.dice_img[val], self.selected_dice_img[val], val, i, count, self.screen_size))

    def set_next_player(self):
        if self.current_player_index == len(self.player_names) - 1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1

    def roll_dice(self, count: int):
        for i in range(0, count):
            # roll dice (1-6)
            rdm = random.randrange(1, 7) 
            self.current_dice.append(dice.Dice(self.dice_img[rdm], self.selected_dice_img[rdm], rdm, i, count, self.screen_size))

    def move(self):
        # reset screen to draw the background image for new dice instances without overlapping
        self.screen.blit(self.background, [0, 0])
        count = 6 - len(self.used_dice)
        self.current_dice.clear()
        self.roll_dice(count) if not self.test_modus else self.use_test_values(count)
        # disable confirm button before any selection
        self.confirm_btn.disable()

    def end_move(self):
        # update score for current player
        self.scores[self.current_player_index].update(len(self.used_dice))
        
        # check if the user can continue with the next move
        if not self.scores[self.current_player_index].continue_move:
            # otherwise it's the next players turn
            self.set_next_player()
        
        # start new first move
        self.used_dice.clear()
        self.move()

    def is_first_move(self):
        return len(self.used_dice) == 0

    def get_selected_current_dice_values(self):
        return [dice.value for dice in self.current_dice if dice.clicked]

    def get_used_dice_values(self):
        return [dice.value for dice in self.used_dice]

    def get_all_selected_dice_values(self):
        res = self.get_selected_current_dice_values() + self.get_used_dice_values()
        return sorted(res, reverse=True)

    def set_selected_dice(self):
        selected_dice_values = self.get_all_selected_dice_values()
        self.used_dice.clear()

        for index, value in enumerate(selected_dice_values):
            self.used_dice.append(draw_only_dice.DrawOnlyDice(self.dice_img[value], value, index, 0.5))
        
    def draw_win_screen(self):
        winner_font = pygame.font.Font(None, 72)
        winner_text = winner_font.render("YOU WIN!" , True, (255, 255, 255))
        winner_rect = winner_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.screen.blit(winner_text, winner_rect)

    def validate(self):
        if validate_selection(self.get_selected_current_dice_values(), self.scores[self.current_player_index], self.is_first_move()):
            self.confirm_btn.enable()
        else:
            self.confirm_btn.disable()

    def handle_confirm_btn(self):
        # draw confirm button and listen to click
        if self.confirm_btn.draw(self.screen):
            self.set_selected_dice()
            self.move()

    def handle_finish_btn(self):
        # draw finish button and listen to click
        if self.finish_btn.draw(self.screen):
            self.end_move()

    def handle_game_play(self):
        if self.scores[self.current_player_index].win:
            self.draw_win_screen()
        else:
            # draw all dice and listen to clicks in object
            for dice in self.current_dice:
                if dice.draw(self.screen):
                    self.validate()

    def show_game_info(self):
        for dice in self.used_dice:
            dice.draw(self.screen)

        # draw score for current player
        self.scores[self.current_player_index].draw(self.screen)        
