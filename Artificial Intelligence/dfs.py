# This program has only recursive appraoch as of now. 
# I have yet to implement the iterative approach. 

# Tree Traversal is of three types:- 
### 1) Preorder (Node -> Left -> Right)
### 2) Postorder (Left -> Right -> Node)
### 3) Inorder (Left -> Node -> Right)

#/// Important Note:- Preorder works only for Binary Trees. 
#/// Postorder and Preorder works for N-ary tree.(using the loops)


# DFS is a search algorithm that expands a node till the end(Null)

# Here, I have implemented Preorder 





from collections import deque

# Tree Node structure
class TreeNode:
    def __init__(self,data):
        self.data = data
        self.childrenNode = []

    def insertChildren(self, nodeList):
        for item in nodeList:
            self.childrenNode.append(item)


# Recursive Approach For Depth First Search in a tree. (Preorder DFS)

def dfs(rootNode ,goalNode, isFound, stack=[], answerList=[]):
    answerList.append(rootNode.data)
    if rootNode.data == goalNode.data:
        return (rootNode, answerList, True)

    else:
        for child in rootNode.childrenNode:
            stack.append(child)

        if len(stack) == 0:
            return (rootNode , answerList, False)
        
        else:
            tempChild = stack.pop()
            return dfs(tempChild, goalNode,False, stack, answerList)

# Function to print the tree.
# def printTree(queue, children=[]):
#     print()
#     for item in children:
#         print(item.data, sep = ' ')
        
#     while queue:
#         node = queue.popleft()
#         children = []
#         for child in node.childrenNode:
#             children.append(child)


#         printTree(queue,children)




    
root = TreeNode('A')
B = TreeNode('B')
C = TreeNode('C')
D = TreeNode('D')
E = TreeNode('E')
F = TreeNode('F')
G = TreeNode('G')
H = TreeNode('H')
I = TreeNode('I')
J = TreeNode('J')
K = TreeNode('K')

root.insertChildren([B,C])
B.insertChildren([D,E])
C.insertChildren([F,G])
D.insertChildren([H])
E.insertChildren([I])
F.insertChildren([J])

queue = deque()
queue.append(root)

# Calling function to check if the goal node is present in the tree or not.
# (rootNode, answerList, isFound) is the tuple returned as result where 
# rootNode   --> last node vistied by the algorithm, 
# answerList --> the path to reach rootNode, and 
# isFound    --> a boolean result that tells if the goal node was found or not.   

result = dfs(root, C, False)  

if (result[2]):
    print("The goal node was found in the tree.")
    print(f"The path is {result[1]}.")

# printTree(queue)







# Iterative Approach is yet to implement.