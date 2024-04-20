def compound_calculator(current_holdings:float,
                        deposit:float,
                        start_age:float,
                        end_age:float,
                        assumed_yearly_growth:float):

    years_to_compound:float = (end_age - start_age) + 1

    assumed_yearly_growth:float = assumed_yearly_growth / 100.0

    months_in_year:float = 12

    yearly_breakdown = {"Year":[], 
                        "Deposits":[],
                        "Cumulative Deposits":[],
                        "Compound Growth":[],
                        "Cumulative Compound Growth":[],
                        "Balance":[]}

    for year in range(years_to_compound):

        if year == 0:

            yearly_breakdown["Year"].append(year)
            yearly_breakdown["Deposits"].append(current_holdings)
            yearly_breakdown["Cumulative Deposits"].append(current_holdings)
            yearly_breakdown["Compound Growth"].append(0)
            yearly_breakdown["Cumulative Compound Growth"].append(0)
            yearly_breakdown["Balance"].append(current_holdings)

        else:
            previous_compounded_return:float = current_holdings if year == 1 else compounded_return
            previous_deposit:float = current_holdings if year == 1 else previous_deposit + (deposit*months_in_year)
            
            compound_principle:float = compound_principle_calc(current_holdings, 
                                                               assumed_yearly_growth, 
                                                               months_in_year, 
                                                               year)
            
            future_value:float = future_value_calc(deposit,
                                                   current_holdings, 
                                                   assumed_yearly_growth, 
                                                   months_in_year, 
                                                   year)
            
            compounded_return:float = compound_principle + future_value

            compound_growth:float = (compounded_return - previous_compounded_return) - (months_in_year * deposit)

            previous_compound_growth:float = compound_growth if year == 1 else previous_compound_growth + compound_growth

            yearly_breakdown["Year"].append(year)
            yearly_breakdown["Deposits"].append(deposit*12)
            yearly_breakdown["Cumulative Deposits"].append(previous_deposit + (deposit*months_in_year))
            yearly_breakdown["Compound Growth"].append(compound_growth)
            yearly_breakdown["Cumulative Compound Growth"].append(previous_compound_growth)
            yearly_breakdown["Balance"].append(compounded_return)
        
        year+=1

    return compounded_return, yearly_breakdown



def compound_principle_calc(current_holdings:float,
                            assumed_yearly_growth:float,
                            months_in_year:float,
                            year:int):
    
    ch = current_holdings
    ayg = assumed_yearly_growth
    miy = months_in_year
    
    compound_principle:float = (1.0 + ayg / miy)**(miy * year)
    compound_principle = compound_principle * ch

    return compound_principle



def future_value_calc(deposit:float,
                      current_holdings:float,
                      assumed_yearly_growth:float,
                      months_in_year:float,
                      year:int):
    
    dep = deposit
    ch = current_holdings
    ayg = assumed_yearly_growth
    miy = months_in_year
    
    future_value:float = ((1.0 + ayg / miy)**(miy * year) - 1.0)
    future_value = future_value / (ayg / miy)
    future_value = future_value * dep

    return future_value
