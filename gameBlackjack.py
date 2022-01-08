import random
import itertools


class Player:
    def __init__(self):
        self.cards_in_hand = []
        self.count = 0


class Dealer(Player):
    def __init__(self):
        self.hole_card = None
        super().__init__()


class Game:
    deck = []
    result = None
    card_types = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    card_points = {
        'J': 10,
        'Q': 10,
        'K': 10,
    }

    player = Player()
    dealer = Dealer()

    def __init__(self):
        self.__create_deck()

    def __create_deck(self):
        self.deck = self.card_types * 4
        random.shuffle(self.deck)

    def __get_value_ace(self, num_ace):
        all_value_ace = itertools.product([1, 11], repeat=num_ace)
        value_ace = [sum(z) for z in all_value_ace if sum(z) <= 21]
        return value_ace

    def __scoring(self, member):
        total = 0
        num_ace = 0
        value_ace = [0]

        for card in member.cards_in_hand:

            if card != 'A':
                total += self.card_points.get(card, card)
            else:
                num_ace += 1

            if num_ace > 0:
                value_ace = self.__get_value_ace(num_ace)

            final_totals = [z+total for z in value_ace if z+total <= 21]
            if not final_totals:
                member.count = total + min(value_ace)
            else:
                member.count = max(final_totals)

    def __clear_values(self):
        self.player.cards_in_hand = []
        self.player.count = 0

        self.dealer.cards_in_hand = []
        self.dealer.count = 0

        self.result = None

    def __display_game_points(self, level=''):
        print('-' * 51)

        if level == 'all':
            print('Карты дилера: {}'.format(self.dealer.cards_in_hand))
            print('Очки дилера: {}'.format(self.dealer.count))
        else:
            print('Карты дилера: {}, *'.format(self.dealer.cards_in_hand[0]))
            print('Очки дилера: *')

        print('Ваши карты: {}'.format(self.player.cards_in_hand))
        print('Ваши очки: {}'.format(self.player.count))

    def __communication_with_player(self, cause):
        correct_input = False
        while not correct_input:
            if cause == 'continue':
                player_desire = input('Продолжить? y/n ')
                if player_desire == 'y' or player_desire == 'n':
                    correct_input = True
            elif cause == 'player_turn':
                player_desire = input('s - stand, h - hit: ')
                if player_desire == 's' or player_desire == 'h':
                    correct_input = True

        return player_desire

    def __calculate_result(self):
        player = self.player.count
        dealer = self.dealer.count
        victory_conditions = [player > dealer or dealer > 21,
                              player <= 21,
                              ]

        if (player > dealer or dealer > 21) and player <= 21:
            return 'player'
        elif (dealer > 21 and player > 21) or dealer == player:
            return 'draw'
        else:
            return 'dealer'

    def start_game(self):
        print('Игра в Blackjack началась')

        while True:
            # Обнулить результаты
            self.__clear_values()

            # Если в колоде меньше 20 карт - создать новую колоду
            if len(self.deck) < 20:
                self.__create_deck()

            # Раздать по две карты игроку и дилеру
            for z in range(2):
                self.player.cards_in_hand.append(self.deck.pop(0))
                self.dealer.cards_in_hand.append(self.deck.pop(0))

            # Скрыть одну карту дилера
            self.dealer.hole_card = self.dealer.cards_in_hand[1]

            # считаем очки игрока и дилера
            self.__scoring(self.player)
            self.__scoring(self.dealer)

            if self.dealer.count == 21:
                self.__display_game_points(level='all')
                if self.player.count == 21:
                    self.result = 'Раунд окончен. Ничья'
                    print(self.result)
                else:
                    self.result = 'Раунд окончен. Вы проиграли'
                    print(self.result)

                player_desire = self.__communication_with_player('continue')

                if player_desire == 'y':
                    continue
                else:
                    break

            while True:
                self.__display_game_points()
                if self.player.count < 21:
                    player_desire = self.__communication_with_player('player_turn')
                else:
                    player_desire = 's'

                if player_desire == 's':
                    print('-' * 51)
                    print('Дилер берет карты')
                    while self.dealer.count < 17:
                        self.dealer.cards_in_hand.append(self.deck.pop(0))
                        self.__scoring(self.dealer)

                    self.__display_game_points(level='all')

                    res = self.__calculate_result()

                    if res == 'player':
                        print('Вы выиграли')
                    elif res == 'dealer':
                        print('Вы проиграли')
                    else:
                        print('Ничья')

                    break

                elif player_desire == 'h':
                    self.player.cards_in_hand.append(self.deck.pop(0))
                    self.__scoring(self.player)

            player_desire = self.__communication_with_player('continue')

            if player_desire == 'y':
                continue
            else:
                break

        print('Игра окончена')
        input()


if __name__ == '__main__':
    game = Game()
    game.start_game()
