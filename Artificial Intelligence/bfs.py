from collections import deque 

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.childrenNodeList = []

    def insertChildren(self, nodeList):
        for node in nodeList:
            self.childrenNodeList.append(node)
    
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

def breadthFirstSearch(Node, goalNode, queue,answerList=[]):
    if Node.data == goalNode.data:
        return (True,answerList)
    
    else:
        for item in Node.childrenNodeList:
            queue.append(item)

        if not queue:
            return (False,answerList)

        temp = queue.popleft()
        answerList.append(temp)

    return breadthFirstSearch(temp,goalNode,queue,answerList)


result = breadthFirstSearch(root, J, queue, [root])

isGoalPresent = result[0]
answerList = result[1]
if isGoalPresent:
    print('The path from the root node to goal node is as follows: ')
    print(len(answerList))
    for item in answerList:
        print(item.data,end=' --> ')
    print('Goal')

else:
    print('The Goal Node is not present in the Tree, so a path can not be found.')
