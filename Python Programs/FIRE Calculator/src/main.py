# Notes
# Have an option to show by currency

def input_current_pension_holdings() -> float:
    current_pension_holdings:str = input("Enter your current pension holdings: ")
    current_pension_holdings:float = float(current_pension_holdings)
    
    return current_pension_holdings


def input_deposits() -> float:
    deposit:str = input("Enter your monthly pension contributions: ")
    deposit:float = float(deposit)
    
    return deposit


def input_current_age() -> float:
    current_age:str = input("Enter your current age (0-100): ")
    current_age:float = float(current_age)
    
    return current_age


def input_age_to_retire() -> float:
    age_to_retire:str = input("Enter your retirement age (0-100): ")
    age_to_retire:float = float(age_to_retire)
    return age_to_retire


def input_assumed_yearly_growth() -> float:
    assumed_yearly_growth:str = input("Enter assumed yearly growth (0.00-100.00): ")
    assumed_yearly_growth:float = float(assumed_yearly_growth)
    return assumed_yearly_growth


def compound_calculator(current_pension_holdings:float,
                        deposit:float,
                        current_age:float,
                        age_to_retire:float,
                        assumed_yearly_growth:float):
    
    years_to_compound:float = age_to_retire - current_age

    assumed_yearly_growth:float = assumed_yearly_growth / 100.0

    compound_principle:float = current_pension_holdings * (1.0 + assumed_yearly_growth / 12.0)**(12.0 * years_to_compound)

    future_value:float = 100.0 * (((1.0 + assumed_yearly_growth / 12.0)**(12.0 * years_to_compound) - 1.0) / (assumed_yearly_growth / 12))

    compounded_return:float = compound_principle + future_value

    return compounded_return



current_pension_holdings = input_current_pension_holdings()
deposit = input_deposits()
current_age = input_current_age()
age_to_retire = input_age_to_retire()
assumed_yearly_growth = input_assumed_yearly_growth()

compounded_return = compound_calculator(current_pension_holdings,
                                        deposit,
                                        current_age,
                                        age_to_retire,
                                        assumed_yearly_growth)

print(compounded_return)








