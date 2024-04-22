from input_functions import *
from compound_function import *
from tabulated_returns import *



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
    pension_total_return = pension_return["Balance"][-1]
    pension_total_contribution = pension_return["Cumulative Deposits"][-1]
    pension_total_compound_return = pension_return["Cumulative Compound Growth"][-1]
    
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
    isa_total_return = isa_return["Balance"][-1]
    isa_total_contribution = isa_return["Cumulative Deposits"][-1]
    isa_total_compound_return = isa_return["Cumulative Compound Growth"][-1]


    print()
    currency_symbol = input_currency_symbol()
    print()

    print("- Pension -")
    print(tabulate_list(pension_return))
    print(f"Total Returns:          {currency_symbol}{round(pension_total_return):,}")
    print(f"Total Contributions:    {currency_symbol}{round(pension_total_contribution):,}")
    print(f"Total Compound Growth:  {currency_symbol}{round(pension_total_compound_return):,}")
    
    
    print()
    print("- ISA -")
    print(tabulate_list(isa_return))
    print(f"Total Returns:          {currency_symbol}{round(isa_total_return):,}")
    print(f"Total Contributions:    {currency_symbol}{round(isa_total_contribution):,}")
    print(f"Total Compound Growth:  {currency_symbol}{round(isa_total_compound_return):,}")



if __name__ == "__main__":
    main()
