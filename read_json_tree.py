from treelib import Node, Tree
import json
def read_json(filename):
    f = open(filename)
    data = json.load(f)

    f.close()
    def to_tuple(lst):
        tuple_ = tuple(to_tuple(i) if isinstance(i, list) else i for i in lst)
        return tuple_
    tuple_ = to_tuple(data)

    tree =Tree()
    tree.create_node('1 Do you want to enter your begining location? or directly search a park?','1 Do you want to enter your begining location? or directly search a park?')

    def show_tree(tuple_):
        if not tuple_[2]:
            if tuple_[1]:
                tree.create_node(tuple_[1],tuple_[1],parent=tuple_[0])
            #tree.create_node(tuple_[2][0],tuple_[2][0],parent=tuple_[0])
            return
        else:
            tree.create_node(tuple_[1][0],tuple_[1][0],parent=tuple_[0])
            tree.create_node(tuple_[2][0],tuple_[2][0],parent=tuple_[0])
            show_tree(tuple_[1])
            show_tree(tuple_[2])
            
    show_tree(tuple_)
    tree.show()


    return tuple_, tree

