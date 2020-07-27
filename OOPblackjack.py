import random
suites = ('♠', '♣', '♥', '♦')
numbers = ('A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K')
bicycle_cards = [(n, s) for n in numbers for s in suites]
face_cards = {
    'J': 10,
    'Q': 10,
    'K': 10,
}


class Deck:
    def __init__(self, stack):
        self.stack = stack  # game_deck = Deck(bicycle_cards)

    def card_exit(self):
        card_drawn = random.choice(self.stack)
        self.stack.remove(card_drawn)
        return card_drawn

    def check_cards(self, player):
        if len(self.stack) <= 12:
            print("Looks like we have played through the available cards!")
            print(f'✨✨✨ Your final score: ${player.chips} ✨✨✨')
            return False
        else:
            return True


class Hand:
    def __init__(self, total_value):
        self.total_value = total_value
        self.in_hand = []

    def draw(self, card_drawn):  # call the card_exit function as an argument to the card_drawn
        self.in_hand.append(card_drawn)
        return card_drawn

    def card_value_add(self, card_drawn):  # call the hit function as an argument to the card_drawn
        if type(card_drawn[0]) == int:
            self.total_value += card_drawn[0]
        elif card_drawn[0] == 'A':
            if type(self) == Player:
                print('Looks like you received an Ace!')
                value = int(input(f'     Choose whether your {card_drawn} will act as 1 or 11: '))
                self.total_value += value
            elif type(self) == Dealer:
                value2 = self.ace_decision()
                self.total_value += value2
        else:
            self.total_value += face_cards.get(card_drawn[0])


class Player(Hand):
    def __init__(self, total_value):
        super().__init__(total_value)   # search up what super init does
        self.chips = 100           # so when you call init function on a sub class
        self.bet_amount = 0                 # ( in this case it was to create the initial variables ),
        # it overrides the parent init function, so you have to refer to parent init again, possibly with super function

    def bet(self, f_bet):
        self.bet_amount = f_bet

    def surrender(self):
        self.bet_amount /= 2
        self.chips -= self.bet_amount
        print(f"Subtracting half of initial bet from player...")

    def double_up(self, insert_deck):
        self.bet_amount *= 2
        self.draw(insert_deck.card_exit())
        self.card_value_add(self.in_hand[-1])
        print('Drawing a card...')
        print(f"Your final hand: {self.in_hand}")

    def blackjack(self):
        jack = self.bet_amount * 1.5
        self.chips += jack
        print('Blackjack!')
        print(f'You win ${jack}!')

    def bust(self):
        print('🔥Bust! Sorry, looks like you lost this round🔥')    # lets see if i can add bust and check to base class
        print(f'Subtracting ${self.bet_amount} from player...')
        self.chips -= self.bet_amount

    def check(self):
        if self.total_value == 21:
            self.blackjack()    # returns nothing which ends game
        elif self.total_value > 21:
            self.bust()
        else:
            return True

    def score_board(self, opponent):
        if self.total_value > opponent.total_value:
            print('🏆Congrats! You win this round🏆')
            print(f'Awarding ${self.bet_amount} to player...')
            self.chips += self.bet_amount
        elif self.total_value < opponent.total_value:
            print('🔥Sorry, looks like you lost this round🔥')
            print(f'Subtracting ${self.bet_amount} from player...')
            self.chips -= self.bet_amount
        else:
            print("❄ Looks like this round ended in a tie ❄")


class Dealer(Hand):    # I don't need an init here cause it just inherent exactly from hand class for initial variables
    def ace_decision(self):
        if 17 <= self.total_value + 11 <= 22:
            return 11
        elif 17 <= self.total_value + 1 <= 22:
            return 1
        elif self.total_value + 11 > 21:
            return 1
        else:
            return 11

    def dealers_start(self, insert_deck):
        for i in range(2):
            self.draw(insert_deck.card_exit())
        print(f"Dealer's hand: [{self.in_hand[0]}, (other card faced down)]")
        self.card_value_add(self.in_hand[0])
        self.card_value_add(self.in_hand[1])

    def house_decision(self, insert_deck, player):
        if self.total_value <= 16:
            # print(f"Dealer's hand so far: {self.in_hand}")
            self.draw(insert_deck.card_exit())
            print(f'Dealer draws a {self.in_hand[-1]}')
            self.card_value_add(self.in_hand[-1])
            return self.dealer_check(player)
        else:
            return False

    def dealer_check(self, player):
        if self.total_value > 21:
            self.dealer_bust(player)
        if self.total_value <= 16:
            return True
        if 16 < self.total_value <= 21:
            return False

    def dealer_bust(self, player):    # static cause no mention of self in the function action
        print('🏆 Dealer busted! You win this round 🏆')
        print(f'Awarding ${player.bet_amount} to player...')
        player.chips += player.bet_amount


instructions = """♦The goal of blackjack is to get closer to 21, without going over, than the dealer.
♦Face cards are worth 10. Aces are worth 1 or 11, the drawer decides.
♦Each player starts with two cards, the dealer's second card is hidden until the player finishes his/her turn.
♦The player plays his/her turn, and only when the player's turn end can the dealer start their turn. 
♦There are only 2 turns in a round. 
♦To 'Hit' is to ask for another card. To 'Stand' is to hold your total and end your turn.
♦Going over 21 means you bust, losing the round.
♦If you get an exact total of 21, you win 1.5x the amount of your bet! 
♦The dealer has to hit themselves until their cards total 17 or higher, even if it causes them to bust.
♦If the dealer's hand totals 17 or higher, their turn automatically ends.
♦You can surrender right after your initial 2 cards are dealt. Surrendering lets you lose only half your bet.
♦"Doubling up" doubles your initial bet, gives you one more card, and then ends your turn for the game.
♦The game ends when there are only 12 cards left in the deck."""
commands = """===== Turn 1 commands: play, help, command, quit =====
---Turn 2 commands: hit, stand, double up, surrender ---"""


def player_moves(player, insert_deck, turn, move):
    # return True if the move does not end the player's turn, return False if it ends player's turn
    if move == 'hit':
        if turn == 1:
            for i in range(2):
                player.draw(insert_deck.card_exit())
            print('Passing out cards...')
            print(f"Your hand: {player.in_hand}")
            player.card_value_add(player.in_hand[0])  # outside the for loop because you want to see your cards first
            player.card_value_add(player.in_hand[1])  # before deciding ace value, since value_add auto calls decision
        else:
            player.draw(insert_deck.card_exit())
            print('Drawing a card...')
            print(f"Your hand: {player.in_hand}")
            player.card_value_add(player.in_hand[-1])
        return player.check()
    elif move == 'stand':
        # print(f"Your final hand: {player.in_hand}")
        return False
    elif move == 'double up':  # doubles bet and then forces user to take 1 and only 1 more card.
        if len(player.in_hand) == 2:
            print('Doubling bet...')
            player.double_up(insert_deck)
            if player.check() is None:
                return None
            return False
        else:
            print('Sorry, you can only double up if you have exactly 2 cards in your hand')
        return True
    elif move == 'surrender':
        player.surrender()
    else:
        print('Invalid Answer')
        return True


def main():
    you = Player(0)
    comp1 = Dealer(0)
    game_deck = Deck(bicycle_cards)   # once deck runs out of cards, the game ends, and shows final chip count
    game = True
    while game:
        print('New round started!')
        you.in_hand = []
        you.total_value = 0
        comp1.in_hand = []
        comp1.total_value = 0
        msg = input('     (turn 1) What would you like to do?: ').lower()
        if msg == 'play':
            run = True
            while run:  # Main inner loop
                print(f'You currently have ${you.chips}')
                money = int(input('     Place your initial bet: $'))
                you.bet(money)
                run = player_moves(you, game_deck, 1, 'hit')   # if run is anything but none, program keeps going
                if run is None:
                    break           # if you don't add break, the rest of the program below will run, just not loop
                comp1.dealers_start(game_deck)
                player_turn = True
                while player_turn:
                    move = input("     (turn 2) What's your next move?: ").lower()
                    player_turn = player_moves(you, game_deck, 2, move)
                    if not player_turn:
                        break
                if player_turn is None:
                    break
                print("-Dealer's Turn-")
                print(f"Turning over dealer's hidden card...  It was a {comp1.in_hand[1]}!")
                # print(f"Dealer's hand: {comp1.in_hand}")
                dealer_turn = True
                while dealer_turn:
                    dealer_turn = comp1.house_decision(game_deck, you)
                if dealer_turn is None:
                    break
                print(f"Dealer's final hand: {comp1.in_hand}")
                you.score_board(comp1)
                break
            game = game_deck.check_cards(you)
        elif msg == 'help':
            print(instructions)
        elif msg == 'command':
            print(commands)
        elif msg == 'quit':
            print('Aw okay, I hope you had fun :)')
            break
        else:
            print('Invalid Answer')


print('♠ Welcome to BlackJack ♠')
print('Type "help" to learn how to play. Type "command" to view available commands')
main()

