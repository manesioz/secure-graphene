from graphql.backend.core import GraphQLCoreBackend

def measure_depth(selection_set, current_depth=1):
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
                raise Exception('Query is too deep')

        return document
