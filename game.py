"""
Project: Blackjack
Author: Vu Tran
Website: http://vu-tran.com/
"""

# import modules

import simplegui, random

# configurations

GAME_WINDOW_WIDTH = 600
GAME_WINDOW_HEIGHT = 600
GAME_WINDOW_SIZE = (GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT)
CARD_IMAGE_SRC = "https://www.dropbox.com/s/cd6ik0pmrnk97nm/cards.png?dl=1" # source URL for the card image
CARD_BACK_IMAGE_SRC = "https://www.dropbox.com/s/t8ib5k3z1uv6w7v/cards-back.png?dl=1"
CARD_IMAGE_SIZE = (72, 96) # the dimensions of the card
HAND_GUTTER_SIZE = 5 # width between each card in the hand
BUTTONS_SIZE = (163, 30) # size of the buttons

class Dispatcher:
    def __init__(self):
        self.events = []
    def add(self, event_name, handler):
        """
        Registers a new event handler
        """
        data = {
            "name": event_name,
            "handler": handler
        }
        self.events.append(data)
    def run(self, name, args):
        """
        Runs all events that matches the given name
        """
        # iterate through all events
        for e in self.events:
            # if it's of the draw type
            if e['name'] == name:
                # call the given handler
                e['handler'](args)

class Frame:
    def __init__(self, frame, size):
        self.frame = frame
        self.size = size
    def get_width(self):
        """
        Returns the width of the frame
        """
        return self.size[0]
    def get_height(self):
        """
        Returns the height of the frame
        """
        return self.size[1]
    def get(self):
        """
        Returns the frame object
        """
        return self.frame
    def start(self):
        """
        Starts the frame
        """
        self.get().start()
    def add_button(self, label, handler):
        """
        Adds a new button to the frame
        """
        self.get().add_button(label, handler)
    def set_draw_handler(self, handler):
        self.get().set_draw_handler(handler)
    def set_mouseclick_handler(self, handler):
        self.get().set_mouseclick_handler(handler)

class Game:
    def __init__(self, size):
        """
        Creates a new game window
        """
        # sets the window's size
        self.set_window_size(size)
        # creates the Frame
        self.frame = self.create_frame()
    def set_window_size(self, size):
        """
        Sets the game window's size

        <tuple> size
        """
        self.window_size = size
    def get_window_size(self):
        """
        Gets the game window's size
        """
        return self.window_size
    def get_window_width(self):
        return self.get_window_size()[0]
    def get_window_height(self):
        return self.get_window_size()[1]
    def create_frame(self):
        """
        Creates and returns a new Frame instance and set's the draw handler
        """
        sg_frame = simplegui.create_frame("Game", self.get_window_width(), self.get_window_height())
        # create a new Frame instance
        frame = Frame(sg_frame, self.get_window_size())
        # sets the draw handler
        frame.set_draw_handler(self.draw)
        # sets the mouse click handler
        frame.set_mouseclick_handler(self.onclick)
        # return the Frame instance
        return frame
    def get_frame(self):
        """
        Retrieve the Frame instance
        """
        return self.frame
    def start(self):
        """
        Starts the game (opens the game frame)
        """
        self.get_frame().get().start()
    def draw(self, canvas):
        """
        Draw handler
        """
        dispatcher.run('draw', canvas)
    def onclick(self, position):
        """
        Mouseclick handler
        """
        dispatcher.run('click', position)

class Deck:
    def __init__(self):
        """
        Creates a new deck of cards
        """
        # set the available suits
        self.SUITS = ('C', 'S', 'H', 'D')
        self.RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
        # builds the deck
        self.cards = self.build()
    def build(self):
        """
        Builds and returns an list of cards
        """
        cards = []
        # for each suit
        for s in self.SUITS:
            # for each rank
            for r in self.RANKS:
                # create a new card
                card = Card(s, r)
                # set's the image src
                card.set_image_src(CARD_IMAGE_SRC)
                # set the back image src
                card.set_back_image_src(CARD_BACK_IMAGE_SRC)
                # set's the card size
                card.set_size(CARD_IMAGE_SIZE)
                # add the new card into the list
                cards.append(card)
        return cards
    def shuffle(self):
        """
        Shuffles the deck
        """
        random.shuffle(self.cards)
    def reset(self):
        """
        Resets the deck
        """
        self.cards = self.build()
    def deal(self):
        """
        Chooses and returns a random card and also removes it from the deck

        Returns a randomly dealt card
        """
        # choose a random index
        rand_index = random.randrange(0, len(self.get_cards()))
        # remove the card from the index
        card = self.get_cards().pop(rand_index)
        return card
    def get_cards(self):
        """
        Retrieve the list of cards
        """
        return self.cards
    def get_rank_index(self, rank):
        """
        Given the rank, find the index in the tuple
        """
        return self.RANKS.index(rank)
    def get_suit_index(self, suit):
        """
        Given the suit, find the index in the tuple
        """
        return self.SUITS.index(suit)
    def calculate_center_position(self, card):
        """
        Calculates the card's center positions
        """
        # retrieve the card size
        size = card.get_size()
        # set the center of the card
        center = (size[0] / 2, size[1] / 2)
        # retrieve the rank index
        rank_index = self.get_rank_index(card.get_rank())
        # retrieve the suit index
        suit_index = self.get_suit_index(card.get_suit())
        # calculate the position of the card
        position = (center[0] + (rank_index * size[0]), center[1] + (suit_index * size[1]))
        return position

class Card:
    def __init__(self, suit, rank, is_shown = False):
        self.is_shown = is_shown
        # sets the card's suit
        self.set_suit(suit)
        # sets the card's rank
        self.set_rank(rank)
    def __str__(self):
        return self.get_suit() + ", " + self.get_rank()
    def set_image_src(self, image_src):
        """
        Sets the tiled-image src
        """
        # load the image
        self.image_src = image_src
        self.image = simplegui.load_image(self.image_src)
    def get_image_src(self):
        """
        Gets the tiled-image src
        """
        return self.image_src
    def get_image(self):
        return self.image
    def set_back_image_src(self, back_image_src):
        self.back_image_src = back_image_src
        self.back_image = simplegui.load_image(self.back_image_src)
    def get_back_image_src(self):
        return self.back_image_src
    def get_back_image(self):
        return self.back_image
    def show(self):
        self.is_shown = True
    def hide(self):
        self.is_shown = False
    def set_size(self, size):
        """
        Sets the size of the card

        <tuple> size
        """
        self.size = size
    def get_size(self):
        """
        Returns the size of the card
        """
        return self.size
    def get_center(self):
        """
        Retrieve the center of the card image (half of the size)
        """
        size = self.get_size()
        return (size[0] / 2, size[1] / 2)
    def set_suit(self, suit):
        self.suit = suit
    def get_suit(self):
        return self.suit
    def set_rank(self, rank):
        self.rank = rank
    def get_rank(self):
        return self.rank
    def get_value(self, use_lower = False):
        """
        Calulates the value of the given card.
        If use_lower is set to True, Aces will count as 1
        instead of 11.

        Returns the possible value of the card
        """
        if self.get_rank() == 'A':
            if use_lower:
                return 1
            else:
                return 11
        elif self.get_rank() in ['J', 'Q', 'K']:
            return 10
        else:
            return int(self.get_rank())
    def set_center_source(self, center_source):
        self.center_source = center_source
    def get_center_source(self):
        return self.center_source
    def set_position(self, position):
        """
        Sets the card's position in the canvas
        """
        self.position = position
    def get_position(self):
        """
        Retrieve the card's position in the canvas
        """
        return self.position
    def get_bounds(self):
        """
        Retrieve the bounding box for the current card (top-left and bottom-right)
        """
        # retrieve the current center position
        position = self.get_position()
        # retrieve the tile's center (half size of the card)
        card_center = self.get_center()
        # calculate the top-left
        topleft = (position[0] - card_center[0], position[1] - card_center[1])
        # calculate the bottom-right
        bottomright = (position[0] + card_center[0], position[1] + card_center[1])
        return (topleft, bottomright)
    def draw(self, canvas):
        """
        Draws the card in the canvas
        """
        # set the image
        image = self.get_image()
        # a pair of coordinates giving the position of the center of the image
        center_source = self.get_center_source()
        # if not shown, set the image to be drawn as the back image
        if not self.is_shown:
            image = self.get_back_image()
            center_source = self.get_center()
        # a pair of integers giving the size of the original image
        width_height_source = self.get_size()
        # a pair of screen coordinates specifying where the center of the image should be drawn on the canvas
        center_dest = self.get_position()
        # a pair of integers giving the size of how the images should be drawn
        width_height_dest = self.get_size()
        canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest)

class Hand:
    def __init__(self, x, y, size, gutter_size):
        self.cards = []
        self.buttons = []
        self.x = x
        self.y = y
        self.size = size
        self.line_width = 1
        self.line_color = 'gray'
        self.fill_color = 'gray'
        self.gutter_size = gutter_size
        self.is_playing = False
        # register the draw handlers
        dispatcher.add('draw', self.draw_background)
        dispatcher.add('draw', self.draw_cards)
    def get_position(self):
        return (self.x, self.y)
    def get_size(self):
        return self.size
    def get_gutter_size(self):
        return self.gutter_size
    def set_deck(self, deck):
        """
        Sets the deck for the given hand
        """
        self.deck = deck
    def get_deck(self):
        """
        Retrieve the deck that is associated to this hand
        """
        return self.deck
    def add_card(self, card):
        self.cards.append(card)
    def get_cards(self):
        return self.cards
    def reset(self):
        """
        Resets the hand
        """
        # reset cards
        self.cards = []
        # reset the playing flag
        self.is_playing = False
    def is_blackjack(self):
        if self.get_value() == 21:
            return True
        return False
    def is_bust(self):
        # if the lower and higher values are over 21
        if self.get_value() > 21 and self.get_value(True) > 21:
            return True
        return False
    def check_hand(self):
        """
        Checks the hand and runs the appropriate handler

        Ends when a blackjack or bust is found
        """
        # check if it's a blackjack
        if self.is_blackjack():
            self.blackjack_handler()
        # else, check if it's a bust
        elif self.is_bust():
            self.bust_handler()
    def hit(self):
        # deal a random card from the deck
        card = self.deck.deal()
        # show the card
        card.show()
        # add the new card to the hand
        self.add_card(card)
        # checks the hand
        self.check_hand()
    def stand(self):
        """
        Ends the turn for the given hand and calls
        the stand handler
        """
        if self.stand_handler:
            self.stand_handler()
    def get_value(self, use_lower = False):
        """
        Calculates the value of the hand.
        If use_lower is set to True, Aces will count
        as 1 instead of 11.

        Returns the largest possible value of the hand
        """
        sum = 0
        for card in self.get_cards():
            sum += card.get_value(use_lower)
        return sum
    def calculate_position(self, card, card_number):
        """
        Calculates and return a tuple representing the position for the given card

        <Card> card             The card
        <int> card_number       The index of the card in the hand
        """
        # retrieve the card size
        size = card.get_size()
        # retrieve the card center
        center = card.get_center()
        # calculate the card's top left corner
        topleft = (center[0] + (size[0] * card_number), center[1])
        # calcualte the gutters
        gutter = self.gutter_size + (self.gutter_size * card_number)
        # calculate the position
        position = (self.x + topleft[0] + gutter, self.y + topleft[1] + self.gutter_size)
        return position
    def draw_cards(self, canvas):
        """
        Draws the cards
        """
        cards = self.get_cards()
        # iterate through each card in the hand
        for i in range(len(cards)):
            # retrieve the current card
            card = cards[i]
            # calculate the card's position
            # set's the image src
            card.set_image_src(CARD_IMAGE_SRC)
            # set's the card size
            card.set_size(CARD_IMAGE_SIZE)
            # set the center source
            card.set_center_source(self.get_deck().calculate_center_position(card))
            # set the position
            card.set_position(self.calculate_position(card, i))
            # draw the card
            card.draw(canvas)
    def draw_background(self, canvas):
        """
        Draws the background
        """
        position = [
            (self.x, self.y), # top left
            (self.x + self.size[0], self.y), # top right
            (self.x + self.size[0], self.y + self.size[1]), # bottom right
            (self.x, self.y + self.size[1]) # bottom left
        ]
        canvas.draw_polygon(position, self.line_width, self.line_color, self.fill_color)
    def set_stand_handler(self, stand_handler):
        self.stand_handler = stand_handler
    def set_blackjack_handler(self, blackjack_handler):
        self.blackjack_handler = blackjack_handler
    def set_bust_handler(self, bust_handler):
        self.bust_handler = bust_handler

class PlayerHand(Hand):
    def deal(self):
        """
        Deals a new hand
        """
        # if currently playing
        if self.is_playing:
            # loses this round and calls the deal new handler
            self.deal_new_handler()
        # resets the deck
        self.deck.reset()
        # resets the hand
        self.reset()
        # deal 2 random cards from the deck
        card1 = self.deck.deal()
        card2 = self.deck.deal()
        card1.show()
        card2.show()
        # add the new card to the hand
        self.add_card(card1)
        self.add_card(card2)
        # enable the playing flag
        self.is_playing = True
        # calls the deal handler
        if self.deal_handler:
            self.deal_handler()
        # checks the current hand
        self.check_hand()
    def set_deal_handler(self, deal_handler):
        self.deal_handler = deal_handler
    def set_deal_new_handler(self, deal_new_handler):
        self.deal_new_handler = deal_new_handler

class AIHand(Hand):
    def start(self):
        """
        Starts the AI hand.

        While the hand is less than 17, keep hitting
        """
        self.is_playing = True
        # display all current cards
        for card in self.get_cards():
            card.show()
        # hit while less than 17
        while self.get_value() < 17:
            self.hit()
        # ends the hand
        self.stand()
    def reset(self):
        """
        Resets the hand
        """
        # calls the parent method
        Hand.reset(self)
        # deals 2 cards faced down
        card1 = self.deck.deal()
        card2 = self.deck.deal()
        card1.show()
        # add the new card to the hand
        self.add_card(card1)
        self.add_card(card2)

class ActionPanel:
    def __init__(self, x, y, buttons_size, gutter_size = 5):
        """
        Creates a new action panel with action buttons: DEAL, HIT, and STAND

        <int> x
        <int> y
        <tuple> buttons_size
        <int> gutter_size
        """
        # set the positions
        self.x = x
        self.y = y
        # set the buttons' size
        self.buttons_size = buttons_size
        # set the gutter size
        self.gutter_size = gutter_size
        # create a dictionary of buttons
        self.buttons = {}
        # register the draw handler
        dispatcher.add('draw', self.draw_buttons)
    def get_buttons_size(self):
        return self.buttons_size
    def add_button(self, name, text, size, handler):
        """
        Creates and return a new button and bind the onclick event with the given handler

        <string> name
        <string> text
        <tuple> size
        <callable> handler
        """
        # create a new button
        button = Button(text, size, self.x, self.y + self.gutter_size, handler)
        # append to dictionary
        self.buttons[name] = button
        return button
    def get_buttons(self):
        return self.buttons
    def get_button(self, key):
        return self.buttons[key]
    def draw_buttons(self, canvas):
        """
        Draws the buttons
        """
        buttons = self.get_buttons()
        # set the counter
        i = 0
        # iterate through each button in the hand
        for key, button in buttons.items():
            # set the button's offset position based on the given index
            button.set_offset(((button.get_width() + self.gutter_size) * i, 0))
            # draw the button
            button.draw(canvas)
            # increment counter
            i += 1

class Button:
    def __init__(self, text, size, x, y, click_handler):
        """
        Creates a new button and draws it on the canvas

        <string> text
        <tuple> size
        <int> c
        <int> y
        <callable> click_handler
        """
        # set the props
        self.text = text
        self.size = size
        self.x = x
        self.y = y
        self.line_width = 1
        self.line_color = "green"
        self.fill_color = "green"
        self.font_size = 16
        self.font_color = "white"
        self.is_disabled = False
        self.click_handler = click_handler
        # register the click handler
        dispatcher.add('click', self.handle_click)
    def get_width(self):
        return self.size[0]
    def get_height(self):
        return self.size[1]
    def set_offset(self, offset):
        """
        Sets an offset

        <tuple> offset
        """
        self.offset = offset
    def get_offset(self):
        return self.offset
    def get_points(self):
        # retrieve the offset
        offset = self.get_offset()
        # calculate the points
        points = [
            (self.x + offset[0], self.y + offset[1]), # top left
            (self.x + self.get_width() + offset[0], self.y + offset[1]), # top right
            (self.x + self.get_width() + offset[0], self.y + self.get_height() + offset[1]), # bottom right
            (self.x + offset[0], self.y + self.get_height() + offset[1]) # bottom left
        ]
        return points
    def disable(self, flag):
        self.is_disabled = flag
    def handle_click(self, position):
        # if not disabled
        if not self.is_disabled:
            # retrieve the points
            points = self.get_points()
            # if x position is within the left/right
            if position[0] >= points[0][0] and position[0] <= points[1][0]:
                # if y position is within the top/bottom
                if position[1] >= points[0][1] and position[1] <= points[2][1]:
                    # calls the stored handler
                    self.click_handler()
    def draw(self, canvas):
        # set the colors
        line_color = self.line_color
        fill_color = self.fill_color
        if self.is_disabled:
            line_color = 'gray'
            fill_color = 'gray'
        # draw the background
        canvas.draw_polygon(self.get_points(), self.line_width, line_color, fill_color)
        # calculate the text width
        text_width = game.get_frame().get().get_canvas_textwidth(self.text, self.font_size)
        # calculate the text positions
        text_pos = (self.get_points()[3][0] + (self.get_width() - text_width) / 2, self.get_points()[3][1] - ((self.get_height() - self.font_size) / 2))
        # draw the text
        canvas.draw_text(self.text, text_pos, self.font_size, self.font_color)

class Score:
    def __init__(self, x, y, size):
        self.wins = 0
        self.losses = 0
        self.x = x
        self.y = y
        self.size = size
        self.display = True
        # register draw handlers
        dispatcher.add('draw', self.draw)
    def set_hand(self, hand):
        self.hand = hand
    def get_hand(self):
        return self.hand
    def get_position(self):
        return (self.x, self.y)
    def get_size(self):
        return self.size
    def inc_wins(self):
        self.wins += 1
    def inc_losses(self):
        self.losses += 1
    def get_wins(self):
        return self.wins
    def get_losses(self):
        return self.losses
    def get_wins_text(self):
        return "Wins: " + str(self.get_wins())
    def get_losses_text(self):
        return "Losses: " + str(self.get_losses())
    def show(self):
        self.display = True
    def hide(self):
        self.display = False
    def draw(self, canvas):
        if self.display:
            # calculate the points of the score in the canvas
            points = [
                (self.x, self.y), # top left
                (self.x + self.size[0], self.y), # top right
                (self.x + self.size[0], self.y + self.size[1]), # bottom right
                (self.x, self.y + self.size[1]), # bottom left
            ]
            # draws the boundary box
            canvas.draw_polygon(points, 1, 'black')
            # draws the text
            font_size = 12
            canvas.draw_text(self.get_wins_text(), (self.x, self.y + ((self.size[1] + font_size) / 2)), font_size, 'white')
            canvas.draw_text(self.get_losses_text(), (self.x + 100, self.y + ((self.size[1] + font_size) / 2)), font_size, 'white')

class Notification:
    def __init__(self, frame, text, font_size = 40):
        """
        Creates a new notification and display it on the canvas
        """
        self.frame = frame
        self.text = text
        self.font_size = font_size
    def draw(self, canvas):
        text_width = self.frame.get().get_canvas_textwidth(self.text, self.font_size)
        point = ((self.frame.get_width() - text_width) / 2, (self.frame.get_height() - self.font_size) / 2)
        canvas.draw_text(self.text, point, self.font_size, 'yellow')

class BlackjackGame(Game):
    def __init__(self, size, hand_gutter_size, buttons_size):
        # calls parent method
        Game.__init__(self, size)
        # creates an empty placeholder prop for notifications
        self.notification = None
        # sets the hand's gutter size
        self.set_hand_gutter_size(hand_gutter_size)
        # set the buttons' size
        self.set_buttons_size(buttons_size)
        # draw the title
        dispatcher.add('draw', self.draw_title)
    def set_hand_gutter_size(self, hand_gutter_size):
        self.hand_gutter_size = hand_gutter_size
    def get_hand_gutter_size(self):
        return self.hand_gutter_size
    def set_buttons_size(self, buttons_size):
        self.buttons_size = buttons_size
    def get_buttons_size(self):
        return self.buttons_size
    def create_deck(self):
        """
        Creates and return a new deck of cards
        """
        deck = Deck()
        return deck
    def create_player_hand(self, deck, score):
        """
        Creates and returns a new player hand and associate
        it with the given deck. The hand will deal from
        the deck

        <Deck> deck
        <Score> score
        """
        # retrieve the score position/size
        score_position = score.get_position()
        score_size = score.get_size()
        # calculate the position of the hand on the canvas (aligned underneath the score)
        x = score_position[0]
        y = score_position[1] + score_size[1] + 5
        size = (500, 106)
        hand = PlayerHand(x, y, size, self.get_hand_gutter_size())
        hand.set_deck(deck)
        return hand
    def create_ai_hand(self, deck, score):
        """
        Creates and returns a new AI hand and associate
        it with the given deck.

        <Deck> deck
        <Score> score
        """
        # retrieve the score position/size
        score_position = score.get_position()
        score_size = score.get_size()
        # calculate the position of the hand on the canvas (aligned underneath the score)
        x = score_position[0]
        y = score_position[1] + score_size[1] + 5
        size = (500, 106)
        hand = AIHand(x, y, size, self.get_hand_gutter_size())
        hand.set_deck(deck)
        return hand
    def create_player_actions(self, hand):
        """
        Creates and returns a new action panel for the player

        <Hand> hand
        """
        # retrieve the hand's positions
        hand_pos = hand.get_position()
        # retrieve the hand's size
        hand_size = hand.get_size()
        # create the player actions
        player_actions = ActionPanel(hand_pos[0], hand_pos[1] + hand_size[1], self.get_buttons_size())
        # create buttons for the panel
        player_actions.add_button('Deal', 'Deal', self.get_buttons_size(), hand.deal)
        player_actions.add_button('Hit', 'Hit', self.get_buttons_size(), hand.hit)
        player_actions.add_button('Stand', 'Stand', self.get_buttons_size(), hand.stand)
        # return the instance
        return player_actions
    def start(self):
        self.deck = self.create_deck()
        # create the score boards
        self.player_score = Score(50, 50, (500, 30))
        self.ai_score = Score(50, 400, (500, 30))
        self.ai_score.hide()
        # create a new player and AI hand
        self.player_hand = self.create_player_hand(self.deck, self.player_score)
        self.player_actions = self.create_player_actions(self.player_hand)
        self.ai_hand = self.create_ai_hand(self.deck, self.ai_score)
        # bind the player and AI hands to the score
        self.player_score.set_hand(self.player_hand)
        # register the handler's for the given hand
        self.player_hand.set_stand_handler(self.handle_player_stand)
        self.player_hand.set_deal_handler(self.handle_player_deal)
        self.player_hand.set_deal_new_handler(self.handle_deal_new)
        self.player_hand.set_blackjack_handler(self.handle_player_blackjack)
        self.player_hand.set_bust_handler(self.handle_player_bust)
        # register AI hand's events
        self.ai_hand.set_stand_handler(self.handle_compare_scores)
        self.ai_hand.set_blackjack_handler(self.handle_player_lost)
        self.ai_hand.set_bust_handler(self.handle_player_win)
        # starts a new game
        self.new_game()
        # create the frame controls
        self.get_frame().add_button('Deal', self.player_hand.deal)
        self.get_frame().add_button('Hit', self.player_hand.hit)
        self.get_frame().add_button('Stand', self.player_hand.stand)
        # display the notification
        self.display_notification('Hit or Stand?')
        dispatcher.add('draw', self.draw_notification)
        # starts the frame
        self.get_frame().start()
    def handle_player_stand(self):
        # enable buttons
        self.player_actions.get_button('Deal').disable(False)
        # disable buttons
        self.player_actions.get_button('Hit').disable(True)
        self.player_actions.get_button('Stand').disable(True)
        # starts the AI hand
        self.ai_hand.start()
    def handle_player_deal(self):
        # enable buttons
        self.player_actions.get_button('Hit').disable(False)
        self.player_actions.get_button('Stand').disable(False)
        # clears the notification
        if self.notification:
            del self.notification
            self.display_notification('Hit or Stand?')
        # resets the AI's hand
        self.ai_hand.reset()
    def handle_player_blackjack(self):
        self.handle_player_win('You won! You have 21! New Deal?')
    def handle_player_bust(self):
        self.handle_player_lost('You lost! You BUSTED! New Deal?');
    def handle_compare_scores(self):
        """
        Compares the player and AI hand
        """
        if self.ai_hand.is_playing:
            if self.ai_hand.is_blackjack():
                self.handle_player_lost('You lost! AI has 21! New Deal?')
            elif self.ai_hand.is_bust():
                self.handle_player_win('You won! AI busted! New Deal?')
            elif max(0, min(21, self.player_hand.get_value())) > max(0, min(21, self.ai_hand.get_value())):
                self.handle_player_win('You won! New Deal?')
            else:
                self.handle_player_lost('You lost! New Deal?')
    def handle_deal_new(self):
        """
        Player chooses to deal a new hand.
        Loses the current hand and deals a new hand.
        """
        if self.player_hand.is_playing and not self.ai_hand.is_playing:
            self.handle_player_lost('You lost! New Deal?')
            self.new_game()
    def handle_player_win(self, message = 'You won! New Deal?'):
        self.player_score.inc_wins()
        self.ai_score.inc_losses()
        # disable buttons
        self.player_actions.get_button('Hit').disable(True)
        self.player_actions.get_button('Stand').disable(True)
        # reset playing flags
        self.player_hand.is_playing = False
        self.ai_hand.is_playing = False
        # display notification
        self.display_notification(message)
    def handle_player_lost(self, message = 'You lost! New Deal?'):
        self.player_score.inc_losses()
        self.ai_score.inc_wins()
        # disable buttons
        self.player_actions.get_button('Hit').disable(True)
        self.player_actions.get_button('Stand').disable(True)
        # reset playing flags
        self.player_hand.is_playing = False
        self.ai_hand.is_playing = False
        # display notification
        self.display_notification(message)
    def new_game(self):
        """
        Starts a new game
        """
        # deals a new hand
        self.player_hand.deal()
    def display_notification(self, text):
        self.notification = Notification(self.get_frame(), text)
    def draw_notification(self, canvas):
        # draw notification if it exists
        if self.notification:
            self.notification.draw(canvas)
    def draw_title(self, canvas):
        text = "Blackjack"
        font_size = 30
        text_width = self.get_frame().get().get_canvas_textwidth(text, font_size)
        point = ((self.get_window_width() - text_width) / 2, font_size + 10)
        canvas.draw_text(text, point, font_size, 'white')



# bootstrap
dispatcher = Dispatcher()
game = BlackjackGame(GAME_WINDOW_SIZE, HAND_GUTTER_SIZE, BUTTONS_SIZE)
game.start()
