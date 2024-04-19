import pandas as pd

def compound_calculator(current_holdings:float,
                        deposit:float,
                        start_age:float,
                        end_age:float,
                        assumed_yearly_growth:float) -> float:
    
    years_to_compound:float = end_age - start_age

    assumed_yearly_growth:float = assumed_yearly_growth / 100.0

    months_in_year:float = 12

    compound_principle:float = current_holdings * (1.0 + assumed_yearly_growth / months_in_year)**(months_in_year * years_to_compound)

    future_value:float = deposit * (((1.0 + assumed_yearly_growth / months_in_year)**(months_in_year * years_to_compound) - 1.0) / (assumed_yearly_growth / months_in_year))

    compounded_return:float = compound_principle + future_value

    return compounded_return



def compound_yearly_breakdown(current_holdings:float,
                              deposit:float,
                              start_age:float,
                              end_age:float,
                              assumed_yearly_growth:float,
                              previous_return:float = None):

    years_to_compound:float = end_age - start_age

    assumed_yearly_growth:float = assumed_yearly_growth / 100.0

    months_in_year:float = 12

    yearly_breakdown = {"Year":[], 
                        "Deposits":[],
                        "Cummulative Deposits":[],
                        "Compound Growth":[],
                        "Cummulative Compound Growth":[],
                        "Balance":[]}
    
    deposit_cumm_list:list = []
    compound_growth_cumm_list:list = []

    
    for year in range(years_to_compound):

        previous_return = current_holdings if previous_return is None else compounded_return
        
        year+=1
        
        compound_principle:float = current_holdings * (1.0 + assumed_yearly_growth / months_in_year)**(months_in_year * year)

        future_value:float = deposit * (((1.0 + assumed_yearly_growth / months_in_year)**(months_in_year * year) - 1.0) / (assumed_yearly_growth / months_in_year))

        compound_growth:float = ((compound_principle+future_value) - previous_return) - (months_in_year*deposit)

        yearly_breakdown["Year"].append(year)
        yearly_breakdown["Deposits"].append(deposit*12)
        yearly_breakdown["Compound Growth"].append(compound_growth)
        yearly_breakdown["Balance"].append(compound_principle + future_value)

        compounded_return:float = compound_principle + future_value

    return compounded_return, yearly_breakdown

compounded_return = compound_yearly_breakdown(25000,
                              2500,
                              34,
                              52,
                              5)

print(compounded_return)


