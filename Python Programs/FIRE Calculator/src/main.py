# Notes
# Have an option to show by currency

# ------------------------------------ functions --------------------------- #

def input_current_holdings(classification:str) -> float:
    current_holdings:str = input(f"Enter your current {classification} holdings: ")
    current_holdings:float = float(current_holdings)
    
    return current_holdings


def input_deposits(classification:str) -> float:
    deposit:str = input(f"Enter your monthly {classification} contributions: ")
    deposit:float = float(deposit)
    
    return deposit


def input_age(classification:str) -> float:
    age:str = input(f"Enter your {classification} age (0-100): ")
    age:float = float(age)
    
    return age


def input_assumed_yearly_growth(classification:str) -> float:
    assumed_yearly_growth:str = input("Enter assumed yearly growth (0.00-100.00) for your {classification}: ")
    assumed_yearly_growth:float = float(assumed_yearly_growth)
    return assumed_yearly_growth


def compound_calculator(current_holdings:float,
                        deposit:float,
                        start_age:float,
                        end_age:float,
                        assumed_yearly_growth:float):
    
    years_to_compound:float = end_age - start_age

    assumed_yearly_growth:float = assumed_yearly_growth / 100.0

    compound_principle:float = current_holdings * (1.0 + assumed_yearly_growth / 12.0)**(12.0 * years_to_compound)

    future_value:float = deposit * (((1.0 + assumed_yearly_growth / 12.0)**(12.0 * years_to_compound) - 1.0) / (assumed_yearly_growth / 12))

    compounded_return:float = round(compound_principle + future_value, 2)

    return compounded_return

# ------------------------------------ main --------------------------------- #
# this the main app function
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


# ------------------------------------ run program ---------------------------#
if __name__ == "__main__":
    main()
