from input_functions import *
from compound_function import *



def main():

    pension_current_holdings = input_current_holdings("Pension")
    pension_deposit = input_deposits("Pension")
    
    current_age = input_age("Current")
    age_to_retire = input_age("Retirement")
    pension_assumed_yearly_growth = input_assumed_yearly_growth("Pension")

    pension_return = compound_calculator(pension_current_holdings,
                                         pension_deposit,
                                         current_age,
                                         age_to_retire,
                                         pension_assumed_yearly_growth)
    pension_compounded_return = pension_return["Balance"][-1]
    
    print()
    isa_current_holdings = input_current_holdings("ISA")
    isa_deposit = input_deposits("ISA")
    
    fire_age = input_age("FIRE")
    isa_assumed_yearly_growth = input_assumed_yearly_growth("ISA")

    isa_return = compound_calculator(isa_current_holdings,
                                     isa_deposit,
                                     current_age,
                                     fire_age,
                                     isa_assumed_yearly_growth)
    isa_compounded_return:float = isa_return["Balance"][-1]


    print()
    currency_symbol = input_currency_symbol()

    print()
    print(f"Your pension returns would be:  {currency_symbol}{round(pension_compounded_return):,}")
    print(f"Your ISA returns would be:      {currency_symbol}{round(isa_compounded_return):,}")



if __name__ == "__main__":
    main()
