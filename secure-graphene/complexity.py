from graphql.backend.core import GraphQLCoreBackend

def calculate_complexity(selection_set, *args): 
    '''
    A function to calculate the complexity of a GraphQL Query    
    
    By default, each field will be assigned a default complexity score of 1, although it can be customized. 
    The function will traverse the query, summing up all the complexity scores for a total. 
    '''
    pass 

