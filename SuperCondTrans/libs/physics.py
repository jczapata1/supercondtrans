# Physics

#--------------------------------------

# Scaling Function
def scaling_func(n, m, TC, T):
    '''
    Generalized scaling function.

    Input:
    -  n (float): n-Critical Exponent 
    -  m (float): m-Critical Exponent
    - TC (float): Critical Temperature
    -  T (float): Temperature

    Output:
    -  f (float): Scaling Function

    Used by:
    - General Proposal
    '''

    f = 1.0 / (1.0 - (T/TC)**n)**m

    return f