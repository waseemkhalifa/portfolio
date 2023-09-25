# ------------------------------------ functions --------------------------- #

# this is our welcome message for the app
def welcome():
    welcome = "Welcome to the Temperature Conversion App"
    return welcome


# we ask for the user to input the temperature in degrees Fahrenheit
def input_fahrenheit():
    fahrenheit = ""
    while fahrenheit.replace(".", "").isnumeric() == False:
        fahrenheit = input("What is the given temperature in degrees Fahrenheit: ")
        if fahrenheit.replace(".", "").isnumeric() == False:
            print()
            print("Input must only contain numeric values!")
            print()
    fahrenheit = float(fahrenheit)
    return fahrenheit 


# this function will convert fahrenheit to celsius
def f_to_c_converter(fahrenheit):
    celsius = (fahrenheit-32) * (5/9)
    return celsius


# this function will convert fahrenheit to kelvin
def f_to_k_converter(fahrenheit):
    kelvin = (fahrenheit-32) * (5/9) + 273.15
    return kelvin


# this is the output message of the program
# it will tell the user the letter occurences in their message
def print_output(fahrenheit, celsius, kelvin):
    fahrenheit = round(fahrenheit, 4)
    celsius = round(celsius, 4)
    kelvin = round(kelvin, 4)

    print(f"Degrees Fahrenheit: \t{fahrenheit}")
    print(f"Degrees Celsius: \t{celsius}")
    print(f"Degrees Kelvin: \t{kelvin}")


# ------------------------------------ main --------------------------------- #
# this the main app function
def main():
    
    # welcome message for our app
    print()
    print(welcome())
    print()

    # we'll ask the user to input fahrenheit
    fahrenheit = input_fahrenheit()

    # we'll convert fahrenheit to celsius
    celsius = f_to_c_converter(fahrenheit)

    # we'll convert fahrenheit to kelvin
    kelvin = f_to_k_converter(fahrenheit)

    # final output
    print_output(fahrenheit, celsius, kelvin)


# ------------------------------------ run program ---------------------------#
if __name__ == "__main__":
    main()
