class Node:
    def __init__(self):
        self.data = None
        self.next = None

head = Node()
temp = head

for i in range(10,101,10):
    tempNode = Node()
    tempNode.data = i
    temp.next = tempNode
    temp = tempNode

current = head.next
while current != None:
    print(current.data, end = '')
    if current.next != None:
        print(' --> ', end = '')
    current = current.next 
    