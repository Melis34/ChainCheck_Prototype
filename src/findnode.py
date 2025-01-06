class FindNode:
    def find_node_by_id(ast, node_id):
        """
        Given the stored AST and a node ID, return the node with the given ID.

        :param node_id: The ID of the node to find.
        :return: The node corresponding to the provided node ID, or None if not found.
        """
        # Helper function to recursively search the AST
        def search_node(node):
            if isinstance(node, dict):
                # If the node has a 'id' and it matches the provided ID, return the node
                if node.get('id') == node_id:
                    return node
                # Otherwise, recursively search in the children
                for key, value in node.items():
                    if isinstance(value, (dict, list)):
                        result = search_node(value)
                        if result:
                            return result
            elif isinstance(node, list):
                # If the node is a list, iterate through its elements
                for item in node:
                    result = search_node(item)
                    if result:
                        return result
            return None

        # Start searching from the root of the AST
        return search_node(ast)

    def find_parent_by_child_id(ast, node_id):
        """
        Given the stored AST and a node ID, return the parent node of the node with the given ID.

        :param node_id: The ID of the child node to find the parent of.
        :return: The parent node of the specified node, or None if not found.
        """
        # Helper function to recursively search for the parent of a given child node
        def search_parent(node, parent=None):
            if isinstance(node, dict):
                # Check if the current node contains the target node ID
                if node.get('id') == node_id:
                    return parent  # Return the parent node
                
                # Otherwise, recursively search in the children
                for key, value in node.items():
                    if isinstance(value, (dict, list)):
                        result = search_parent(value, node)  # Pass current node as the parent
                        if result:
                            return result
            elif isinstance(node, list):
                # If it's a list, iterate through each item and search for parent
                for item in node:
                    result = search_parent(item, parent)
                    if result:
                        return result
            return None

        # Start searching from the root of the AST, with no parent initially
        return search_parent(ast, None)


    def check_for_declarations(ast, declaration):
        def search_node(node):
            if isinstance(node, dict):
                    # If the node has a 'id' and it matches the provided ID, return the node
                    if node.get('declarations') and isinstance(node.get('declarations'), list):
                        for declaration_node in node.get('declarations'):
                            if declaration_node is not None and declaration_node.get('name') == declaration:
                                return node

                    # Otherwise, recursively search in the children
                    for key, value in node.items():
                        if isinstance(value, (dict, list)):
                            result = search_node(value)
                            if result:
                                return result
            elif isinstance(node, list):
                    # If the node is a list, iterate through its elements
                    for item in node:
                        result = search_node(item)
                        if result:
                            return result
                        
        return search_node(ast)

        # Start searching from the root of the AST