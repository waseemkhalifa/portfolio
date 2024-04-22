# ------------------------------------ functions --------------------------- #

# this is our welcome message for the app
def welcome():
    welcome = "Welcome to the letter counter app"
    return welcome


# we ask for the user's name
def input_user_name():
    name = input("What is your name: ")
    return name


# this will title and strip white space of a string
def title_whitespace(name):
    # converts the input string to proper case or title case. 
    # that is, all words begin with uppercase and the rest are lowercase.
    name = name.title().strip()
    name = " ".join(name.split())
    return name


# we welcome the user with a message here with their name
def hello_name(name):
    output_string = f"Hello, {name}!"
    return output_string


# this message will let a user know what the app does
def app_explanation():
    explanation = "I will count the number of times that a specific letter"\
          " occurs in a message."
    return explanation


# this function will ask the user for a message
def input_message():
    message = input("Please enter a message: ")
    return message


# this function will ask the user which letter they'd like to count
# in their message
def input_letter_to_count():
    letter = input("Which letter would you like to count the occurrences of: ")
    return letter


# this function will return a count of occurences of a letter
# inside of a message that's supplied
def count_letter_occurence(letter, message):
    letter = letter.lower()
    message = message.lower()
    count_of_letters = message.count(letter)
    return count_of_letters


# this is the output message of the program
# it will tell the user the letter occurences in their message
def app_output(name, letter, count_of_letters):
    output_string = f"{name}, your message has {count_of_letters} {letter}'s "\
                        "in it."
    return output_string


# ------------------------------------ main --------------------------------- #
# this the main app function
def main():
    
    # welcome message for our app
    print()
    print(welcome())
    print()

    # we'll ask the user to input their name
    # we'll also clean up
    name = input_user_name()
    name = title_whitespace(name)

    # we'll print out the name entered
    print()
    print(hello_name(name))
    
    # we'll print out the app explanation
    print()
    print(app_explanation())
    print()

    # we'll ask the user to input a message
    message = input_message()
    print()

    # we'll ask the user what letter they'd like to count
    letter = input_letter_to_count()

    # this will count the occurances of the letter
    count_of_letters = count_letter_occurence(letter, message)

    # final output
    print()
    print(app_output(name, letter, count_of_letters))
    print()


# ------------------------------------ run program ---------------------------#
if __name__ == "__main__":
    main()
