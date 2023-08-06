"""
My random playground
author: https://github.com/PyOctoCat
date: 3/18/2020
"""

# Reference material
# https://faker.readthedocs.io/en/master/
# https://pypi.org/project/googletrans/
import random
import time
from faker import Faker
# from faker.providers import BaseProvider
# from googletrans import Translator
from strgen import StringGenerator
# import re
import sys
from termcolor import colored


class RandomPlayGround:
    """
    Define methods for random creation and selection functions.
    """
    def __init__(self):
        """
        Vars that need to be available each time a method is called again
        """
        self.used_list = []

    def exhaustive_random(self, source_list, length=1, **args):
        """
        Pick a random item from a list until source list is empty and then start over again.
        Supply a tuple to keep the list immutable so list can be repopulated.
        If a percentage string is supplied calculate value and convert to integer.
        :return:  random item
        """
        # Allow for a percentage value to be supplied
        if '%' in str(length):
            length = round(float(source_list.__len__()) * float(length.strip('%')) / 100.0)
            # Assume at least one was requested
            if length == 0:
                length = 1

        # Using tuple to keep the list immutable
        if type(source_list) is tuple:
            source_list = list(source_list)
        else:
            print('Please supply the list as a tuple to keep it immutable, not a "{}"\n'.format(type(source_list)))
            quit()

        if source_list.__len__() < length:
            print('Length requested of \'{}\' exceeded length of source list({})'.format(length, source_list.__len__()))
            quit()

        # Pick items requested
        the_chosen = []
        for item in range(length):
            # See if used list needs filling
            if not self.used_list:
                if not source_list:
                    print('Please supply a list element, this looks empty!', source_list)
                    quit()
                # print('filling up again', source_list)
                self.used_list = source_list

            # Add to items to be returned
            one_item = RandomPlayGround.choose_from_list(self.used_list, length=1)[0]
            the_chosen.append(one_item)

            # Remove from used up list
            self.used_list.remove(one_item)

        return the_chosen

    @staticmethod
    def makeup_wwn(wwn_method=None, *args):
        """
        Generate a random WWN.
        :return:  WWN
        """
        # http://standards.ieee.org/develop/regauth/oui/oui.txt
        # Sample of Brocade WWNs
        brocade_ouis = ['00:60:69', '00:05:1E', '08:00:88', '00:05:33', '50:EB:1A', '00:27:F8', '00:01:0F', '00:00:88',
                       '00:60:DF', '00:14:C9', 'C4:F5:7C']
        # Random OUI choice
        wwn_oui = random.choice(brocade_ouis).lower()
        wwn_methods = ['1', '2', '5']
        fake_wwn = None

        if wwn_method is None:
            wwn_method = random.choice(wwn_methods)

        if wwn_method not in wwn_methods:
            print('Choose one of these methods {}'.format(wwn_methods))
            quit()

        if wwn_method is '1':
            # IEEE Standard
            wwn_prefix = '10:00'
            # Random suffix of 0x00-0xff, with o hex padding
            wwn_suffix = "{:02x}".format(random.randint(0, 255), 'x') + ':' \
                        + "{:02x}".format(random.randint(0, 255), 'x') + ':' \
                        + "{:02x}".format(random.randint(0, 255), 'x')
            fake_wwn = wwn_prefix + ':' + wwn_oui + ':' + wwn_suffix

        if wwn_method is '2':
            # IEEE Standard
            wwn_prefix = '2' + format(random.randint(0, 15), 'x') + ':' \
                        + "{:02x}".format(random.randint(0, 255), 'x')
            # Random suffix of 0x00-0xff
            wwn_suffix = "{:02x}".format(random.randint(0, 255), 'x') + \
                        ':' + "{:02x}".format(random.randint(0, 255), 'x') + ':' \
                        + "{:02x}".format(random.randint(0, 255), 'x')
            fake_wwn = wwn_prefix + ':' + wwn_oui + ':' + wwn_suffix

        if wwn_method is '5':
            # IEEE Standard
            wwn_prefix = '5'
            wwn_oui = 'B:CD:00:5'
            # Random suffix of 0x00-0xff
            wwn_suffix = format(random.randint(0, 15), 'x') + ':' + "{:02x}".format(random.randint(0, 255),
                                                                                   'x') + ':' + "{:02x}".format(
                random.randint(0, 255), 'x') + ':' + "{:02x}".format(random.randint(0, 255),
                                                                     'x') + ':' + "{:02x}".format(
                random.randint(0, 255), 'x')
            fake_wwn = wwn_prefix + wwn_oui + wwn_suffix

        return fake_wwn

    @staticmethod
    def rex_gen(rex_arg):
        """
        Repackage string generator render functionality to generate words based on regexp pattern
        :return:  regexp word
        :example: Playground.rex_gen('[a-zA-Z0-9]{19}')
        """
        rex_word = StringGenerator(rex_arg).render()
        return rex_word

    @staticmethod
    def choose_number(minimum=0, maximum=1, **args):
        """
        Pick a random number between these numbers, defaults to boolean test
        Have the numbers the same type for minimum and maximum
        If you want hex return use this:  hex(choose_number(minimum=0x0, maximum=0x15)),
        otherwise you can supply int or floating
        :return: random value within range
        """
        if isinstance(minimum, int) and isinstance(maximum, int):
            return random.randint(minimum, maximum)
        elif isinstance(minimum, float) and isinstance(maximum, float):
            # Create random floating value with precision given
            decimals = max(str(minimum).split('.')[1].__len__(), str(maximum).split('.')[1].__len__())
            return round(random.uniform(minimum, maximum), decimals)

    @staticmethod
    def choose_from_list(from_list, length=None, unique=True, **args):
        """
        Pick a random item from a list.
        Supply none, integer or a percentage value
        unique: to True to make sure you don't get the same item twice
        length: None means no restrictions or all
        :return:  random item
        """
        # rnd_domains = fake.random_elements(elements=(domain_list), length=None, unique=True)
        # If number length is percent return that amount
        if '%' in str(length):
            length = round(float(from_list.__len__()) * float(length.strip('%')) / 100.0)
            # Assume at least one was requested
            if length == 0:
                length = 1
        fake = Faker("en_US")
        return fake.random_elements(elements=from_list, length=length, unique=unique)

    @staticmethod
    def randomize_list(from_this, **args):
        """
        Randomize sequence sent to it.
        Right now just randomizing list
        :return:  random item
        """

        # Choose what type of list this is; dic, list...
        if isinstance(from_this, list):
            #  random.shuffle(myList)
            random.shuffle(from_this)
            return from_this

    @staticmethod
    def word_gen(word_size, word_lang='en_US', camelcase=True, **args):
        """
        Generate a random word that is funner than just random letters
        :return:  random word
        """
        fake = Faker(word_lang)

        # Pick a real word to return. Concatenate words if needed
        fake_word = ''
        while str(fake_word).__len__() != word_size:
            # Generate a word, can't specify size yet
            gen_word = fake.word()

            # If we got it right off then we are done
            if str(gen_word).__len__() == word_size or str(fake_word).__len__() == word_size:
                fake_word = gen_word
                break

            # If off by a letter than just add one to make this faster
            if str(fake_word).__len__() == word_size - 1:
                fake_word = fake_word + RandomPlayGround.rex_gen('[a-z]{1}')

            # If off by two letters add two to make this faster
            if str(fake_word).__len__() == word_size - 2:
                if camelcase:
                    fake_word = fake_word + str(RandomPlayGround.rex_gen('[a-z]{2}').title())
                else:
                    fake_word = fake_word + RandomPlayGround.rex_gen('[a-z]{2}')

            # If partial made, then keep on trying to add other words to it
            if str(gen_word).__len__() <= word_size - str(fake_word).__len__():
                if camelcase:
                    fake_word = fake_word + gen_word.title()
                else:
                    fake_word = fake_word + gen_word

        # print('Return', fake_word)
        return str(fake_word)


if __name__ == '__main__':
    print('\nSelf Tests:')
    # play = Progress(max_bar=30)
    # print('Spinning Wheel:')
    # for i in range(16):
    #     play.wheel()
    #     time.sleep(.1)
    # print('\nProgress bar:')
    # for i in range(100):
    #     play.progress_bar()
    #     time.sleep(.05)
    select = RandomPlayGround()
    test_list = ['a', 'b', 'c']
    print('')
    for i in range(7):
        print("Exhaustive:", select.exhaustive_random(tuple(test_list), length=1))
    print('Fake WWN:', RandomPlayGround.makeup_wwn())
    print('Regexp gen:',  RandomPlayGround.rex_gen('[a-zA-Z0-9 _]{8-16}'))
    print('Rnd Decimal:', RandomPlayGround.choose_number(minimum=13.3, maximum=99.0))
    print('Choose from:', test_list, ':', RandomPlayGround.choose_from_list(test_list)[0])
    print('Random real word:', RandomPlayGround.word_gen(RandomPlayGround.choose_number(minimum=3, maximum=13)))

