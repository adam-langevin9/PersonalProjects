import os

GREEN = 'g'
YELLOW = 'y'
WRONG = ' '
DEFAULT_FILE = 'WordleWords.txt'
CWD = os.getcwd()
FILE_NOT_FOUND_MESSAGE = f'Ensure that your wordle words file is in the current working directory. Your current working directory is {CWD}'
START_MESSAGE = 'Good Starter words are slice, tried, or crane'
GUESS_PROMPT = 'Enter your guess: '
GUESS_ERROR = 'Invalid guess: Your guess must be 5 letters'
REENTER_GUESS = 'guess'
HINTS_PROMPT = 'Enter your hints: '
HINTS_ERROR = 'Invalid hints: Your hints should be 5 letters'
HINTS_KEY = f'({GREEN} = green, {YELLOW} = yellow, {WRONG} = wrong, {REENTER_GUESS} = re-enter guess)'
WIN_MESSAGE = "Well Done!"
LOOSE_MESSAGE = "Better Luck Next Time"
FILE_ERROR = f"Unable to load words file: {DEFAULT_FILE}"
DIRECTIONS = f'Start by entering your first 5 letter guess. \nThen enter the corresponding hints you receive using the following key \n{HINTS_KEY}. \nThe system will show you a list of possible words given your guess and hints. \nRepeat this process to get closser to the mystery word. \nBe smart about your choices because you only have 6 tries.'


class WordleHelper:

    def __init__(self, words_file: str = DEFAULT_FILE):
        self.__words_file = words_file
        self.__words = None
        self.__ui = self.UserInput()
        self.__cur_guess = None
        self.__cur_hints = None

    def __completion_check(self):
        if self.__is_win():
            self.__show(WIN_MESSAGE)
        else:
            self.__show(LOOSE_MESSAGE)

    def __import_words(self, file: str):
        try:
            with open(file) as words:
                return set(word.strip() for word in words)
        except FileNotFoundError as e:

            return None

    def __is_win(self):
        return self.__cur_hints == GREEN*5

    def __narrow_words(self):

        def __is_not_word(self, let_count, word, idx, let):
            return (self.__cur_hints[idx] == WRONG and let in word and let_count[let] <= 1) or \
                (self.__cur_hints[idx] == GREEN and let != word[idx]) or \
                (self.__cur_hints[idx] == YELLOW and let not in word) or \
                (self.__cur_hints[idx] == YELLOW and let == word[idx])

        temp_words = tuple(self.__words)
        let_count = OccurrenceDictionary(self.__cur_guess)

        for word in temp_words:
            for idx, let in enumerate(self.__cur_guess):
                if __is_not_word(self, let_count, word, idx, let):
                    self.__words.remove(word)
                    break
                let_count[let] -= 1

    def __show(self, msg):
        print(msg)

    def __show_words(self, cols=10):
        count = 0
        for word in self.__words:
            count += 1
            if count % cols == 0:
                print(word)
            else:
                print(word, end='\t')
        if count % cols != 0:
            print()

    def change_file(self, file: str):
        try:
            with open(file) as words:
                self.__words_file = file
                self.__words = set(word.strip() for word in words)
                return True
        except FileNotFoundError:
            print(FILE_NOT_FOUND_MESSAGE)
            return False

    def start(self):
        self.__words = self.__import_words(self.__words_file)
        self.__cur_guess = None
        self.__cur_hints = None
        if self.__words:
            self.__show(DIRECTIONS)
            self.__show(START_MESSAGE)
            guess_count = 0
            while guess_count < 6 and not self.__is_win():
                self.__cur_guess, self.__cur_hints = self.__ui.probe()
                self.__narrow_words()
                self.__show_words()
            self.__completion_check()

    class UserInput:

        def __init__(self):
            self.guess = ""
            self.hints = ""

        def __user_guess(self):
            self.guess = input(GUESS_PROMPT).lower()
            while len(self.guess) != 5 or not self.guess.isalpha():
                print(GUESS_ERROR)
                self.guess = input(GUESS_PROMPT).lower()
            self.__user_hints()

        def __user_hints(self):

            def valid_hints(hints):
                valid_hints = {GREEN, YELLOW, WRONG}
                if len(self.hints) == 5:
                    if all([letter in valid_hints for letter in self.hints]):
                        return True
                    if self.hints == REENTER_GUESS:
                        return True
                return False

            self.hints = input(HINTS_PROMPT).lower()

            while not valid_hints(self.hints):
                print(HINTS_ERROR)
                print(HINTS_KEY)
                self.hints = input(HINTS_PROMPT).lower()

            if self.hints == REENTER_GUESS:
                self.__user_guess()

        def probe(self):
            self.__user_guess()
            return self.guess, self.hints


class OccurrenceDictionary:

    def __init__(self, word):
        self.occ_dict = {}
        word_letters = set(word)
        for letter in word_letters:
            self.occ_dict[letter] = 0
        for letter in word:
            self.occ_dict[letter] += 1

    def __getitem__(self, key):
        return self.occ_dict[key]

    def __setitem__(self, key, value):
        self.occ_dict[key] = value


def main():
    helper = WordleHelper()
    helper.start()


if __name__ == "__main__":
    main()
