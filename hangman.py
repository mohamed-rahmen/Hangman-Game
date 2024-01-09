from hangman_helper import *

letter_repetition = 0


def update_word_pattern(word, pattern, letter):
    """
    a function that gets a letter from the user, and appends it to its right
    place according to
    its place in the original word
    :param word: A random word that changes every game (until the game ends)
    :param pattern: a pattern with the current guessed letters
    :param letter: the letter that the user guessed
    :return: returns a new updated pattern with the new letter inside it
    """
    new_pattern = ""
    global letter_repetition
    letter_repetition = 0
    for i in range(len(pattern)):
        if word[i] == letter:
            new_pattern += word[i]
            letter_repetition += 1
        elif pattern[i].isalpha():
            new_pattern += pattern[i]
        else:
            new_pattern += "_"
    return new_pattern


def run_single_game(words_list, score):
    """
    This function runs a single game when its called, it runs a single game of
    the well-known game
    hangman, a game that let's a player guess letters as long as their score
    is higher than 0
    :param words_list:
    :param score:
    :return: return the player last score
    """
    guessed_letters = []
    wrong_letters = []
    rand_word = get_random_word(words_list)
    pattern = "_" * len(rand_word)
    length_of_guessed = 0
    display_state(pattern, wrong_letters, score, "")
    while score != 0 and length_of_guessed != len(rand_word):
        player_choice, value = get_input()
        if player_choice == LETTER and (
                len(value) > 1 or value.isalpha() is False or value.isupper()):
            display_state(pattern, wrong_letters, score, "Letter is invalid")
            continue
        if player_choice == LETTER and (
                value in guessed_letters or value in wrong_letters):
            display_state(pattern, wrong_letters, score,
                          "Letter is already guessed")
            continue
        score += -1
        if player_choice == LETTER:
            if value in rand_word:
                length_of_guessed, pattern, score = isLetter(guessed_letters,
                                                             length_of_guessed,
                                                             pattern,
                                                             rand_word,
                                                             score, value,
                                                             wrong_letters)
                continue
            else:
                wrong_letters.append(value)
                if score == 0:
                    break
                display_state(pattern, wrong_letters, score,
                              "you guessed a wrong letter")

                continue
        if player_choice == WORD:
            n = len(rand_word) - length_of_guessed
            if value == rand_word:
                score = score + n * (n + 1) // 2
                pattern = rand_word
                break
            if score > 0:
                display_state(pattern, wrong_letters, score,
                              "you guessed a wrong word")
        if player_choice == HINT:
            show_suggestions(
                filter_words_list(words_list, pattern, wrong_letters))
            continue

    if score == 0:
        msg = "you lost the word was " + rand_word
        display_state(pattern, wrong_letters, score, msg)
    else:
        display_state(pattern, wrong_letters, score, "You won the game")
        pass
    return score


def isLetter(guessed_letters, length_of_guessed, pattern, rand_word, score,
             value, wrong_letters):
    """
    A function that is called inside the run_single_game function, that
    if the player's choice is a letter, it checks if it is inside the
    random_word, whether it was guessed before or not, if not and if it was
     inside
    the word, it adds it using the update_word_pattern function
    :param guessed_letters: a list of letters that the player already guessed
    :param length_of_guessed: the amount of letters that the user guessed right
    :param rand_word: a random word that the user gets in the beginning of
     each run
    :param score: the player's current score
    :param value: the letter that the user guessed
    :param wrong_letters: the list of letters that were wrongly guessed
    :return:returns the edited length of guessed, with an edited pattern and
     a modified score
    """
    global letter_repetition
    pattern = update_word_pattern(rand_word, pattern, value)
    score = score + letter_repetition * (letter_repetition + 1) // 2
    guessed_letters.append(value)
    length_of_guessed += letter_repetition
    if length_of_guessed != len(pattern):
        display_state(pattern, wrong_letters, score,
                      "you guessed a right letter")

    return length_of_guessed, pattern, score


def main():
    """
    a main function that is used to run the game, and let's the user play more
    than once, with their
    score, and amount of played games saved
    :return:
    """
    global letter_repetition
    lst_words = load_words()
    score = run_single_game(lst_words, POINTS_INITIAL)
    counter = 1
    msg = "you played so far: " + str(counter) + "your score is: " + str(score)
    while play_again(msg):
        letter_repetition = 0
        if score <= 0:
            counter = 1
            score = run_single_game(lst_words, POINTS_INITIAL)
            msg = "you played so far: " + str(
                counter) + "your score is: " + str(score)
        if score > 0:
            counter += 1
            score = run_single_game(lst_words, score)
            msg = "you played so far: " + str(
                counter) + "your score is: " + str(score)
        if score <= 0:
            msg = "you survived " + str(counter)


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    a function that let's the user ask for help, by typing "?",
    when this symbol is shown,
    this function gets called by the run_single_game function,
    and then it shows the player
    an amount of hints that fits certain criterias
    :param words:the complete list of words that the letter was taken from
    :param pattern:the pattern with current guessed letters, in order to help
    find words that fit the cirteria
    :param wrong_guess_lst:a list with guessed wrong letters, in order to
    remove those words from the hints
    :return:
    """
    lst = []
    boolean = False
    counter = 0
    visible_letters = 0

    for letter in pattern:
        if letter.isalpha():
            visible_letters += 1
    if visible_letters == 0:
        for hints in words:
            for wrong_letter in wrong_guess_lst:
                if wrong_letter in hints:
                    boolean = True
            if not boolean:
                if len(hints) == len(pattern):
                    lst.append(hints)
            boolean = False

    else:
        boolean = False
        for i in words:
            for wrong_letter in wrong_guess_lst:
                if wrong_letter in i:
                    boolean = True

            if len(i) == len(pattern) and boolean is False:

                for j in range(len(pattern)):

                    if i.count(pattern[j]) == pattern.count(pattern[j]) and \
                            pattern[j].isalpha() and pattern[j] == i[j]:
                        counter += 1

            if visible_letters == counter:
                lst.append(i)
            counter = 0
            boolean = False
    newlst = []
    counter = 0
    lst_len = len(lst)
    if len(lst) > HINT_LENGTH:
        while len(newlst) != HINT_LENGTH:
            newlst.append(lst[(counter * lst_len) // HINT_LENGTH])
            counter += 1
    else:
        newlst = lst
    return newlst


if __name__ == '__main__':
    main()
