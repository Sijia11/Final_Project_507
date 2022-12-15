import json
from treelib import Node, Tree
mapTree = \
    ("1 Do you want to enter your begining location? or directly search a park?",
        ("2 Please type your beginning location",
            ("3 Your distance is limited to 350 miles",
            ("4 Your cloud percentage is at most 20%", None, None),
            ("5 Your cloud percentage is at most 10%", None, None)), 
            ("6 Your distance is not limited to 350 miles", ("7 Your cloud percentage is at most 20%", None, None),
            ("8 Your cloud percentage is at most 10%", None, None))),
        ("9 Please type your search place", ("10 Your cloud percentage is at most 20%", None, None),
            ("11 Your cloud percentage is at most 10%", None, None)))

res = []

def ask_map(tree, answer, i):
    global res
    res = []
    def helper(tree, answer, i):

        if not tree[2]:
            cur_tree = tree
            tree = (cur_tree[0], "final request:" + str(res), None)
            return tree
        else:
            if answer[i] == "1":
                res.append(tree[1][0])
                return (tree[0], helper(tree[1], answer, i + 1), tree[2])
            elif answer[i] == "2":
                res.append(tree[2][0])
                return (tree[0], tree[1], helper(tree[2], answer, i + 1))
            else:
                res[-1] += " " + answer[i]
                return helper(tree, answer,i+1)
    return helper(tree,answer,i), res




def save_json(filename,tree):
    jsonobject = json.dumps(tree)
    fw = open(filename,"w")
    fw.write(jsonobject)
    fw.close() 




# def read_json(filename):
#     f = open(filename)
#     data = json.load(f)

#     f.close()
#     def to_tuple(lst):
#         tuple_ = tuple(to_tuple(i) if isinstance(i, list) else i for i in lst)
#         return tuple_
#     tuple_ = to_tuple(data)

#     tree =Tree()
#     tree.create_node('1 Do you want to enter your begining location? or directly search a park?','1 Do you want to enter your begining location? or directly search a park?')

#     def show_tree(tuple_):
#         if not tuple_[2]:
#             if tuple_[1]:
#                 tree.create_node(tuple_[1],tuple_[1],parent=tuple_[0])
   
#             return
#         else:
#             tree.create_node(tuple_[1][0],tuple_[1][0],parent=tuple_[0])
#             tree.show()
#             tree.create_node(tuple_[2][0],tuple_[2][0],parent=tuple_[0])
#             show_tree(tuple_[1])
#             show_tree(tuple_[2])
            
#     show_tree(tuple_)
#     tree.show()


#     return tuple_, tree

