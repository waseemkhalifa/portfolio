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

    compounded_return:float = round(compound_principle + future_value, 2)

    return compounded_return
