'''
This python program stores self-defined functions for general purposes.
'''

from numpy import arange

def series_generation(From = 0, To = 0, Num_of_pt = 1, rev_concat = False) -> list:
    '''
    rev_concat means whether the user want to concatanate the reversed list after the original list.
    e.g.1
    Input  ---> From = 100, To = 0, Num_of_pt = 2, rev_concat = False
    Output ---> [100.0, 0.0]

    e.g.2
    Input  ---> From = 100, To = 0, Num_of_pt = 2, rev_concat = True
    Output ---> [100.0, 0.0, 0.0, 100.0]
    '''
    if Num_of_pt <= 1: # prevent meaningless num_of_pt
        return [From]
    step = (To - From) / (Num_of_pt - 1)
    if rev_concat == False:
        return list(arange(From, To + step, step))
    else:
        forth = list(arange(From, To + step, step))
        back = list(reversed(forth))
        return forth + back

if __name__ == "__main__":
    print(series_generation(From = 100, To = 0, Num_of_pt = 2, rev_concat = False))
