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
CARD_IMAGE_SRC = "https://www.dropbox.com/s/cd6ik0pmrnk97nm/cards.png?dl=1" # source URL for the card image
CARD_IMAGE_SIZE = (72, 96) # the dimensions of the card
HAND_GUTTER_SIZE = 5 # width between each card in the hand

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

class Game:
    def __init__(self, size):
        """
        Creates a new game window
        """
        # create an empty list of events
        self.events = []
        # sets the window's size
        self.set_window_size(size)
        # creates the game frame (window)
        self.create_frame()
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
        Creates a new game frame (window) and set's the draw handler
        """
        self.frame = simplegui.create_frame("Game", self.get_window_width(), self.get_window_height())
        # sets the draw handler
        self.frame.set_draw_handler(self.draw)
        # sets the mouse click handler
        self.frame.set_mouseclick_handler(self.onclick)
    def get_frame(self):
        return self.frame
    def start(self):
        """
        Starts the game (opens the game frame)
        """
        self.frame.start()
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
    def draw(self, canvas):
        pass

class Card:
    def __init__(self, suit, rank):
        # sets the card's suit
        self.set_suit(suit)
        # sets the card's rank
        self.set_rank(rank)
        # register the click
        dispatcher.add('click', self.onclick)
    def __str__(self):
        return self.get_suit() + ", " + self.get_rank()
    def onclick(self, position):
        """
        Onclick handler for the given card
        """
        #bounds = self.get_bounds()
        #print bounds
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
        image = self.get_image()
        # a pair of coordinates giving the position of the center of the image
        center_source = self.get_center_source()
        # a pair of integers giving the size of the original image
        width_height_source = self.get_size()
        # a pair of screen coordinates specifying where the center of the image should be drawn on the canvas
        center_dest = self.get_position()
        # a pair of integers giving the size of how the images should be drawn
        width_height_dest = self.get_size()
        canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest)

class Hand:
    def __init__(self, x, y, width, height, gutter_size):
        self.cards = []
        self.buttons = []
        self.x = x
        self. y = y
        self.width = width
        self.height = height
        self.line_width = 1
        self.line_color = 'gray'
        self.fill_color = 'gray'
        self.gutter_size = gutter_size
        # draws the action buttons
        self.add_button('Hit', 150, 30, self.hit)
        self.add_button('Stand', 150, 30, self.stand)
        # register the draw handler
        dispatcher.add('draw', self.draw_background)
        dispatcher.add('draw', self.draw_cards)
        dispatcher.add('draw', self.draw_buttons)
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
    def add_button(self, text, width, height, handler):
        """
        Creates a new button and bind the onclick event with the given handler
        """
        # create a new button
        button = Button(text, width, height, self.x + self.width + self.gutter_size, self.y, handler)
        self.buttons.append(button)
    def get_buttons(self):
        return self.buttons
    def deal(self):
        """
        Deals a random card from the deck for the hand
        """
        card = random.choice(self.deck.get_cards())
        self.add_card(card)
    def hit(self):
        pass
    def stand(self):
        # TODO
        pass
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
        topleft = (center[0] + (size[0] * card_number), center[1] + (size[1] * card_number))
        # calcualte the gutters
        gutter = self.gutter_size + (self.gutter_size * card_number)
        # calculate the position
        position = (self.x + topleft[0] + gutter, self.y + topleft[1] + gutter)
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
            (self.x + self.width, self.y), # top right
            (self.x + self.width, self.y + self.height), # bottom right
            (self.x, self.y + self.height) # bottom left
        ]
        canvas.draw_polygon(position, self.line_width, self.line_color, self.fill_color)
    def draw_buttons(self, canvas):
        """
        Draws the buttons
        """
        buttons = self.get_buttons()
        # iterate through each card in the hand
        for i in range(len(buttons)):
            # retrieve the button
            button = buttons[i]
            # set the button's offset position based on the given index
            button.set_offset((0, (button.get_height() + self.gutter_size) * i))
            # draw the button
            button.draw(canvas)


class Button:
    def __init__(self, text, width, height, x, y, handler):
        """
        Creates a new button and draws it on the canvas
        """
        # set the props
        self.text = text
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.line_width = 1
        self.line_color = "green"
        self.fill_color = "green"
        self.font_size = 16
        self.font_color = "white"
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def set_offset(self, offset):
        self.offset = offset
    def get_offset(self):
        return self.offset
    def get_points(self):
        # retrieve the offset
        offset = self.get_offset()
        # calculate the points
        points = [
            (self.x + offset[0], self.y + offset[1]), # top left
            (self.x + self.width + offset[0], self.y + offset[1]), # top right
            (self.x + self.width + offset[0], self.y + self.height + offset[1]), # bottom right
            (self.x + offset[0], self.y + self.height + offset[1]) # bottom left
        ]
        return points
    def draw(self, canvas):
        # draw the background
        canvas.draw_polygon(self.get_points(), self.line_width, self.line_color, self.fill_color)
        # calculate the text width
        text_width = game.get_frame().get_canvas_textwidth(self.text, self.font_size)
        # calculate the text positions
        text_pos = (self.get_points()[3][0] + (self.get_width() - text_width) / 2, self.get_points()[3][1] - ((self.get_height() - self.font_size) / 2))
        # draw the text
        canvas.draw_text(self.text, text_pos, self.font_size, self.font_color)

class BlackjackGame(Game):
    def __init__(self, size, hand_gutter_size):
        # create an empty list of events
        self.events = []
        # sets the window's size
        self.set_window_size(size)
        # creates the game frame (window)
        self.create_frame()
        # sets the hand's gutter size
        self.set_hand_gutter_size(hand_gutter_size)
    def set_hand_gutter_size(self, hand_gutter_size):
        self.hand_gutter_size = hand_gutter_size
    def get_hand_gutter_size(self):
        return self.hand_gutter_size
    def create_deck(self):
        """
        Creates and return a new deck of cards
        """
        deck = Deck()
        return deck
    def create_hand(self, deck):
        """
        Creates and returns a new hand and associate
        if with the given deck. The hand will deal from
        the deck
        """
        x = 50
        y = 50
        width = 360
        height = 106
        hand = Hand(x, y, width, height, self.get_hand_gutter_size())
        hand.set_deck(deck)
        return hand
    def start(self):
        self.deck = self.create_deck()
        # register the deck's draw handler
        self.hand = self.create_hand(self.deck)
        # deals the first card
        self.hand.deal()
        # starts the frame
        self.frame.start()


# bootstrap

dispatcher = Dispatcher()

game = BlackjackGame((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT), HAND_GUTTER_SIZE)
game.start()
