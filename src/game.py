import pygame
import random
import src.button as button
import src.dice as dice
import src.draw_only_dice as draw_only_dice
import src.score as score
from src.validator import validate_selection


WIN_MSG = "YOU WIN!"

class Game():
    def __init__(self, screen_size: tuple(), player_names: [str], caption: str):
        self.screen_size = screen_size
        self.player_names = player_names

        self.__init_game(caption)
        self.__init_buttons()
        self.__init_scores()
        self.__init_dice()
        
        # start first move
        self.__move()

    def handle_buttons(self):
        if self.scores[self.current_player_index].win:
            self.__handle_new_game_btn()
            self.__handle_end_game_btn()
        else:
            self.__handle_confirm_move_btn()
            self.__handle_finish_move_btn()

    def handle_game_play(self):
        if self.scores[self.current_player_index].win:
            self.__draw_win_screen()
        else:
            # draw all dice and listen to clicks in object
            for dice in self.current_dice:
                if dice.draw(self.screen):
                    self.__validate()

    def show_game_info(self):
        # draw used dice
        for dice in self.used_dice:
            dice.draw(self.screen)

        # draw score for current player
        self.scores[self.current_player_index].draw(self.screen)

    """ ----- Private Functions ----- """

    """ --- Init Functions --- """

    def __init_game(self, caption: str):
        # global init (needed for fonts etc.)
        pygame.init()
        # set game name
        pygame.display.set_caption(caption)
        #create display window
        self.screen = pygame.display.set_mode(self.screen_size)
        # init background image
        self.background = pygame.image.load('img/table_top.png').convert_alpha()        

    def __init_buttons(self):
        # init button images
        confirm_move_btn_enabled_img = pygame.image.load('img/button_confirm-move.png').convert_alpha()
        confirm_move_btn_disabled_img = pygame.image.load('img/disabled_button_confirm-move.png').convert_alpha()
        finish_move_btn_img = pygame.image.load('img/button_end-move.png').convert_alpha()
        new_game_btn_img = pygame.image.load('img/button_new-game.png').convert_alpha()
        end_game_btn_img = pygame.image.load('img/button_end-game.png').convert_alpha()

        # init global button instances
        self.confirm_move_btn = button.Button(confirm_move_btn_enabled_img, 1, "right", self.screen_size, confirm_move_btn_disabled_img)
        self.finish_move_btn = button.Button(finish_move_btn_img, 1, "left", self.screen_size)
        self.new_game_btn = button.Button(new_game_btn_img, 1, "right", self.screen_size)
        self.end_game_btn = button.Button(end_game_btn_img, 1, "left", self.screen_size)

    def __init_scores(self):
        # init scores for all players
        self.current_player_index = 0
        self.scores = []
        for player_name in self.player_names:
            self.scores.append(score.Score(player_name, self.screen_size[0]))

    def __init_dice(self):
        # init dice images
        self.dice_img = {}
        self.selected_dice_img = {}
        for i in range(1, 7):
            self.dice_img[i] = pygame.image.load('img/' + str(i) + '.png').convert_alpha()
            self.selected_dice_img[i] = pygame.image.load('img/' + str(i) + '_selected.png').convert_alpha()
        
        # init empty dice instances
        self.current_dice = []
        self.used_dice = []        

    """ --- Button Functions --- """

    def __handle_confirm_move_btn(self):
        # draw confirm button and listen to click
        if self.confirm_move_btn.draw(self.screen):
            self.__set_selected_dice()
            self.__move()

    def __handle_finish_move_btn(self):
        # draw finish button and listen to click
        if self.finish_move_btn.draw(self.screen):
            self.__end_move()

    def __handle_new_game_btn(self):
        if self.new_game_btn.draw(self.screen):
            self.__init_scores()
            self.__move()

    def __handle_end_game_btn(self):
        if self.end_game_btn.draw(self.screen):
            quit_event = pygame.event.Event(pygame.QUIT)
            pygame.event.post(quit_event)

    """ --- Dice Functions --- """

    def __roll_dice(self, count: int):
        for i in range(0, count):
            # roll dice (1-6)
            rdm = random.randrange(1, 7) 
            self.current_dice.append(dice.Dice(self.dice_img[rdm], self.selected_dice_img[rdm], rdm, i, count, self.screen_size))

    def __is_first_move(self):
        return len(self.used_dice) == 0

    def __get_selected_current_dice_values(self):
        return [dice.value for dice in self.current_dice if dice.clicked]

    def __get_used_dice_values(self):
        return [dice.value for dice in self.used_dice]

    def __get_all_selected_dice_values(self):
        res = self.__get_selected_current_dice_values() + self.__get_used_dice_values()
        return sorted(res, reverse=True)

    def __set_selected_dice(self):
        selected_dice_values = self.__get_all_selected_dice_values()
        self.used_dice.clear()

        for index, value in enumerate(selected_dice_values):
            self.used_dice.append(draw_only_dice.DrawOnlyDice(self.dice_img[value], value, index, 0.5))

    """ --- Game Functions --- """

    def __set_next_player(self):
        if self.current_player_index == len(self.player_names) - 1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1

    def __move(self):
        # reset screen to draw the background image for new dice instances without overlapping
        self.screen.blit(self.background, [0, 0])
        count = 6 - len(self.used_dice)
        self.current_dice.clear()
        self.__roll_dice(count)
        # disable confirm button before any selection
        self.confirm_move_btn.disable()

    def __end_move(self):
        # update score for current player
        self.scores[self.current_player_index].update(len(self.used_dice))
        
        # check if the user can continue with the next move
        if not self.scores[self.current_player_index].continue_move:
            # otherwise it's the next players turn
            self.__set_next_player()
        
        # start new first move
        self.used_dice.clear()
        self.__move()
        
    def __draw_win_screen(self):
        winner_font = pygame.font.Font(None, 72)
        winner_text = winner_font.render(WIN_MSG , True, (255, 255, 255))
        winner_rect = winner_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.screen.blit(winner_text, winner_rect)

    def __validate(self):
        if validate_selection(self.__get_selected_current_dice_values(), self.scores[self.current_player_index], self.__is_first_move()):
            self.confirm_move_btn.enable()
        else:
            self.confirm_move_btn.disable()
