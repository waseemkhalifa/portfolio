# ------------------------------------ functions --------------------------- #

# this is our welcome message for the app
def welcome():
    welcome = "Welcome to the Miles Per Hour Conversion App"
    return welcome


# we ask for the user to input miles per hour
def input_mph():
    mph = ""
    while mph.replace(".", "").isnumeric() == False:
        mph = input("What is your speed in miles per hour: ")
        if mph.replace(".", "").isnumeric() == False:
            print()
            print("Input must only contain numeric values!")
            print()
    mph = float(mph)
    return mph 


# this function will convert the miles per hour to meters per second
def mph_converter(mph):
    mps = mph * 0.4474
    mps = round(mps, 2)
    return mps


# this is the output message of the program
# it will tell the user the letter occurences in their message
def app_output(mps):
    output_string = f"Your speed in meters per second is {mps}"
    return output_string


# ------------------------------------ main --------------------------------- #
# this the main app function
def main():
    
    # welcome message for our app
    print()
    print(welcome())
    print()

    # we'll ask the user to input mph
    mph = input_mph()

    # this will convert the mph to mps
    mps = mph_converter(mph)

    # final output
    print(app_output(mps))


# ------------------------------------ run program ---------------------------#
if __name__ == "__main__":
    main()
