from compound_function import *
from tabulate import tabulate



def tabulate_list(dictionary:dict):

    dictionary_combined_list:list = combine_dictionary_lists(dictionary)

    rows_list:list = list_as_rows(dictionary_combined_list)

    tabulated_list = tabulate(rows_list, 
                              headers=dictionary.keys(),
                              tablefmt="fancy_outline",
                              floatfmt=",.2f",
                              intfmt=",")

    return tabulated_list



def combine_dictionary_lists(pension_return:dict) -> list:
    combined:list = []

    for key in pension_return:
        combined.append(pension_return[key])
    
    return combined



def list_as_rows(combined_dictionary_list:list) -> list:
    rows_list:list = []

    for a in range(len(combined_dictionary_list)):
        for b in range(len(combined_dictionary_list[a])):
            rows_list.append([item[b] for item in combined_dictionary_list])
        break
    
    return rows_list
