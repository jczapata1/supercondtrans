# Decorators
from time import perf_counter

#---------------------------------------------------------------------------------------------------------

# Benchmark
def benchmark(function):
    '''
    Measure performance metrics of a function.
    
    Input:
    - function (callable): Function
    
    Output:
    -  wrapper (callable): Wrapper

    Used by:
    - General Proposal
    '''

    # Wrapper
    def wrapper(*args, **kwargs):
        
        ti            = perf_counter()             # Initial Time
        result        = function(*args, **kwargs)  # Execute Base Function
        tf            = perf_counter()             # Final Time
        wrapper.time  = round(tf - ti, 2)          # Total Time
        class_name    = args[0].__class__.__name__ # Class Name
        function_name = function.__name__          # Function Name
        print(f'{class_name:>14} - {function_name.title().replace('_', ' '):>21}: {wrapper.time:7.2f} s')
        
        return result

    return wrapper