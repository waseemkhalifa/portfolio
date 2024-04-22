def input_current_holdings(classification:str) -> float:
    while True:
        current_holdings:str = input(f"Enter your current {classification} holdings: ")
        
        try:
            current_holdings:float = float(current_holdings)
            break
        except ValueError:
            print(f"{current_holdings} is an unacceptable input, please enter a numerical value")
    
    return current_holdings



def input_deposits(classification:str) -> float:
    while True:
        deposit:str = input(f"Enter your monthly {classification} contributions: ")
        
        try:
            deposit:float = float(deposit)
            break
        except ValueError:
            print(f"{deposit} is an unacceptable input, please enter a numerical value")
    
    return deposit



def input_age(classification:str) -> int:
    while True:
        age:str = input(f"Enter your {classification} age (0-100): ")
        
        try:
            age:int = int(age)
            break
        except ValueError:
            print(f"{age} is an unacceptable input, please enter a whole number")

    return age



def input_assumed_yearly_growth(classification:str) -> float:
    while True:
        assumed_yearly_growth:str = input(f"Enter assumed yearly % growth (0.00-100.00) for your {classification}: ")
        
        try:
            assumed_yearly_growth:float = float(assumed_yearly_growth)
            break
        except ValueError:
            print(f"{assumed_yearly_growth} is an unacceptable input, please enter a numerical value")
            
    return assumed_yearly_growth



def input_currency_symbol() -> float:
    acceptable_input:list[str] = ["$", "€", "£", "₹", "¥"]

    while True:
            currency_symbol:str = input("Enter the currency you'd like to see your results in ($, €, £, ₹, ¥): ")
            if any(currency_symbol in x for x in acceptable_input) & len(currency_symbol.strip()) == 1:
                break
            else:
                print(f"{currency_symbol} is an unacceptable input, please enter one of the following: ($, €, £, ₹, ¥)")
            
    return currency_symbol
