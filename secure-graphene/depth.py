from graphql.backend.core import GraphQLCoreBackend

def measure_depth(selection_set, current_depth=1):
    '''
    A function which recursively measures the depth of a Graphene Query
    
    :type selection_set: SelectionSet 
    :param selection_set: Graphql-core object used for query traversal/indexing  
    
    :type current_depth: int 
    :param current_depth: The current depth of the query 
    
    :rtype: int 
    :return: The max depth of the query  
    '''
    max_depth = current_depth
    for field in selection_set.selections:
        if field.selection_set:
            new_depth = measure_depth(field.selection_set, current_depth=current_depth + 1)
            if new_depth > max_depth:
                max_depth = new_depth
    return max_depth

class DepthAnalysisBackend(GraphQLCoreBackend, max_depth):
    def document_from_string(self, schema, document_string):
        document = super().document_from_string(schema, document_string)
        ast = document.document_ast
        for definition in ast.definitions:
            depth = measure_depth(definition.selection_set)
            if depth > max_depth: 
                raise Exception('Query is too deep - its depth is {} but the max depth is {}'.format(depth, max_depth))

        return document
