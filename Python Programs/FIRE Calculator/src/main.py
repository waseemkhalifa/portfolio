from input_functions import *
from compound_function import *

def main():

    current_pension_holdings = input_current_holdings("Pension")
    deposit = input_deposits("Pension")
    current_age = input_age("Current")
    age_to_retire = input_age("Retirement")
    assumed_yearly_growth = input_assumed_yearly_growth("Pension")

    compounded_return = compound_calculator(current_pension_holdings,
                                            deposit,
                                            current_age,
                                            age_to_retire,
                                            assumed_yearly_growth)

    print()
    print(compounded_return)



if __name__ == "__main__":
    main()
