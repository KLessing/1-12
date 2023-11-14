import pygame
import random

from utils.validations import validate_selection
from utils.globals import MAX_DICE_COUNT

from .button import Button
from .dice import Dice
from .draw_only_dice import DrawOnlyDice
from .score import Score
from .dice_comb_selection import DiceCombSelection

CAPTION = "1 - 12"
WIN_MSG = "YOU WIN!"

class Game():
    def __init__(self, screen_size: tuple()):
        self.screen_size = screen_size
        self.game_state = "init"

    def handle_game_state(self):
        match self.game_state:
            case "init":
                self.__handle_init_state()
            case "play":
                self.__handle_play_state()
            case "select":
                self.handle_selection_state()
            case "win":
                self.handle_win_state()

    """ ----- Private Functions ----- """

    """ --- Draw Functions --- """

    def __draw_blank(self):
        self.screen.blit(self.background, [0, 0])
    
    def __draw_dice(self):
        for dice in self.current_dice:
            if dice.draw(self.screen):
                self.__validate()
    
    def __draw_used_dice(self):
        for dice in self.used_dice:
            dice.draw(self.screen)

    def __draw_scores(self):
        for index in range(self.player_count):
            self.scores[index].draw(self.screen)

    def __draw_win_screen(self):
        winner_font = pygame.font.Font(None, 72)
        winner_text = winner_font.render(WIN_MSG , True, (255, 255, 255))
        winner_rect = winner_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.screen.blit(winner_text, winner_rect)            

    """ --- Handler Functions --- """

    def __handle_init_state(self):
        # TODO start game after player count selection
        self.__start_game(2)

    def __handle_play_state(self):
        self.__handle_confirm_move_btn()
        self.__handle_finish_move_btn()
        self.__draw_dice()
        self.__draw_used_dice()
        self.__draw_scores()

    def handle_selection_state(self):
        self.__handle_selection_btns()

    def handle_win_state(self):
        self.__handle_new_game_btn()
        self.__handle_end_game_btn()
        self.__draw_win_screen()

    """ --- Start State --- """

    def start_selection_state(self, single_selection):
        # start selection for single and double combination
        self.selected_double_number = single_selection
        self.end_move_btn.disable()
        self.game_state = "select"        

    """ --- Init Functions --- """

    def __init_all(self):
        self.__init_game(CAPTION)
        self.__init_buttons()
        self.__init_scores()
        self.__init_dice()

    def __init_game(self, caption: str):
        # global init (needed for fonts etc.)
        pygame.init()
        # set game name
        pygame.display.set_caption(caption)
        #create display window
        self.screen = pygame.display.set_mode(self.screen_size)
        # init background image
        self.background = pygame.image.load('img/background_1280px.jpg').convert_alpha()

    def __init_buttons(self):
        # init button images
        confirm_move_btn_enabled_img = pygame.image.load('img/button_confirm-move.png').convert_alpha()
        confirm_move_btn_disabled_img = pygame.image.load('img/disabled_button_confirm-move.png').convert_alpha()
        end_move_btn_enabled_img = pygame.image.load('img/button_end-move.png').convert_alpha()
        end_move_btn_disabled_img = pygame.image.load('img/disabled_button_end-move.png').convert_alpha()
        new_game_btn_img = pygame.image.load('img/button_new-game.png').convert_alpha()
        end_game_btn_img = pygame.image.load('img/button_end-game.png').convert_alpha()

        # init global button instances
        self.confirm_move_btn = Button(confirm_move_btn_enabled_img, 1, "right", self.screen_size, confirm_move_btn_disabled_img)
        self.end_move_btn = Button(end_move_btn_enabled_img, 1, "left", self.screen_size, end_move_btn_disabled_img)
        self.new_game_btn = Button(new_game_btn_img, 1, "right", self.screen_size)
        self.end_game_btn = Button(end_game_btn_img, 1, "left", self.screen_size)

        self.dice_comb_selection = DiceCombSelection(self.screen_size)
        self.selected_double_number = None

    def __init_scores(self):
        # init scores for all players
        self.current_player_index = 0
        self.scores = []
        for index in range(self.player_count):
            self.scores.append(Score(index, self.screen_size[0]))
        self.scores[self.current_player_index].set_active(True)

    def __init_dice(self):
        # init dice images
        self.dice_img = {}
        self.selected_dice_img = {}
        for i in range(1, MAX_DICE_COUNT + 1):
            self.dice_img[i] = pygame.image.load('img/' + str(i) + '.png').convert_alpha()
            self.selected_dice_img[i] = pygame.image.load('img/' + str(i) + '_selected.png').convert_alpha()
        
        # init empty dice instances
        self.current_dice = []
        self.used_dice = []
        # needed for multiple possible combinations for first move (4 + 4 = 4 or 8)
        self.validated_combinations = set()

    """ --- Button Functions --- """

    def __handle_confirm_move_btn(self):
        # draw confirm button and listen to click
        if self.confirm_move_btn.draw(self.screen):
            self.__set_selected_dice()
            self.__move()

    def __handle_finish_move_btn(self):
        # draw finish button and listen to click
        if self.end_move_btn.draw(self.screen):
            self.__end_move()

    def __handle_new_game_btn(self):
        if self.new_game_btn.draw(self.screen):
            self.__init_scores()
            self.__move()

    def __handle_end_game_btn(self):
        if self.end_game_btn.draw(self.screen):
            quit_event = pygame.event.Event(pygame.QUIT)
            pygame.event.post(quit_event)

    def __handle_selection_btn(self, number: int):
        if self.selected_double_number and self.dice_comb_selection.draw(number, self.screen):
            self.scores[self.current_player_index].set_selection(number)
            self.validated_combinations = {number}
            self.selected_double_number = None
            self.game_state = "play"
            self.end_move_btn.enable()
            self.__move()

    # choose between single and comb selection for two identical selections (e.g. 4 and 4 = 4 or 8)
    def __handle_selection_btns(self):
        self.__draw_blank()
        self.__draw_scores()        
        lowest_number = self.selected_double_number
        self.__handle_selection_btn(lowest_number)
        self.__handle_selection_btn(lowest_number * 2)
        
    """ --- Dice Functions --- """

    def __roll_dice(self, count: int):
        for i in range(0, count):
            # roll dice (1-6)
            rdm = random.randrange(1, MAX_DICE_COUNT + 1)
            self.current_dice.append(Dice(self.dice_img[rdm], self.selected_dice_img[rdm], rdm, i, count, self.screen_size))

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
            self.used_dice.append(DrawOnlyDice(self.dice_img[value], value, index, 0.5))

    """ --- Game Functions --- """

    def __start_game(self, player_count):
        self.player_count = player_count
        self.__init_all()
        # start first move
        self.__move()
        self.game_state = "play"

    def __set_next_player(self):
        if self.current_player_index == self.player_count - 1:
            self.current_player_index = 0
        else:
            self.current_player_index += 1

    def __move(self):
        # reset screen to draw the background image for new dice instances without overlapping
        self.__draw_blank()
        # disable confirm button before any selection
        self.confirm_move_btn.disable()

        if len(self.validated_combinations) >= 1:
            single_selection = min(self.validated_combinations)

        if len(self.validated_combinations) >= 2:
            self.start_selection_state(single_selection)
            # stop move for selection
            return
        else:
            # set single selection value when not already set
            if len(self.validated_combinations) == 1 and single_selection != self.scores[self.current_player_index].current_selection:
                self.scores[self.current_player_index].set_selection(single_selection)

        count = MAX_DICE_COUNT - len(self.used_dice)
        self.current_dice.clear()
        self.__roll_dice(count)

        # not first move?
        if len(self.used_dice) > 0:
            # update score for current player
            self.scores[self.current_player_index].update(len(self.used_dice))
            # is the current selection completely collected?
            if self.scores[self.current_player_index].is_selection_complete():
                #  end current move but keep player for next move
                self.__end_move(True)
            # are all dice used?
            elif len(self.used_dice) == MAX_DICE_COUNT:
                # end current move but keep player and selection for next move
                self.__end_move(True, True)

    def __end_move(self, continue_move: bool = False, keep_selection: bool = False):
        # reset selections for current player
        if not keep_selection:
            self.validated_combinations = set()
            self.scores[self.current_player_index].set_selection()

        # check if the user can continue with the next move
        if not continue_move:
            self.scores[self.current_player_index].set_active(False)
            self.__set_next_player()
            self.scores[self.current_player_index].set_active(True)

        # start new first move
        self.scores[self.current_player_index].reset_collected_count()
        self.used_dice.clear()
        self.__move()

    # TODO use once before win state
    # update global negative score for all players who lost
    def __update_global_score(self):
        for index, score in enumerate(self.scores):
            if index != self.current_player_index:
                score.calc_global_score()
        
    def __validate(self):
        selection = self.__get_selected_current_dice_values()
        current_score: Score = self.scores[self.current_player_index]

        if len(selection) > 0:
            prev_selected = {} if current_score.current_selection == None else {current_score.current_selection}
            valid_combinations: set() = validate_selection(selection, prev_selected, current_score.get_completed_values())
            if len(valid_combinations) >= 1:
                self.validated_combinations = valid_combinations

        if len(selection) > 0 and len(valid_combinations) > 0:
            self.confirm_move_btn.enable()
        else:
            self.confirm_move_btn.disable()
