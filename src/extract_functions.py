# extract_functions.py

def extract_functions_from_ast(ast):
    """
    This function will extract all the function definitions from the AST.
    """
    functions = []
    
    # Traverse the AST to find function definitions
    def traverse(node):
        if node['nodeType'] == 'FunctionDefinition':
            # print(node)
            functions.append(node)
        if 'nodes' in node:
            for child_node in node['nodes']:
                
                traverse(child_node)
        elif 'body' in node:
            
            traverse(node['body'])
    
    traverse(ast)
    # print(functions)
    return functions
