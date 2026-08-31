$ git show 03026e8c8212c4b3e4a19c2c2a4914568e0e26c9
commit 03026e8c8212c4b3e4a19c2c2a4914568e0e26c9
Author: Divyam Prasad <divyamprasad.official@gmail.com>
Date:   Wed Aug 26 23:39:49 2026 +0530

    RuntimeError: deque mutated during iteration --- while printing the tree

diff --git a/dfs.py b/dfs.py
new file mode 100644
index 0000000..13268ad
--- /dev/null
+++ b/dfs.py
@@ -0,0 +1,82 @@
+from collections import deque
+
+# Tree Node structure
+class TreeNode:
+    def __init__(self,data):
+        self.data = data
+        self.childrenNode = []
+
+    def insertChildren(self, nodeList):
+        for item in nodeList:
+            self.childrenNode.append(item)
+
+
+# Recursive Approach For Depth First Search in a tree. 
+def dfs(rootNode ,goalNode, isFound, stack=[], answerList=[]):
+
+    answerList.append(rootNode.data)
+
+    if rootNode.data == goalNode.data:
+        return (rootNode, answerList, True)
+
+    else:
+        for child in rootNode.childrenNode:
+            stack.append(child)
+
+        if len(stack) == 0:
+            return (rootNode , answerList, False)
+        
+        else:
+            tempChild = stack.pop()
+            return dfs(tempChild, goalNode,False, stack, answerList)
+
+# Function to print the tree.
+def printTree(queue):
+
+    for node in queue:
+        print(node.data)
+        queue.popleft()
+        for child in node.childrenNode:
+            queue.append(child)
+
+    printTree(queue)
+
+
+
+
+    
+root = TreeNode('A')
+B = TreeNode('B')
+C = TreeNode('C')
+D = TreeNode('D')
+E = TreeNode('E')
+F = TreeNode('F')
+G = TreeNode('G')
+H = TreeNode('H')
+I = TreeNode('I')
+J = TreeNode('J')
+K = TreeNode('K')
+
+root.insertChildren([B,C])
+B.insertChildren([D,E])
+C.insertChildren([F,G])
+D.insertChildren([H])
+E.insertChildren([I])
+F.insertChildren([J])
+
+queue = deque()
+queue.append(root)
+
+# Calling function to check if the goal node is present in the tree or not. 
+result = dfs(root, C, False)
+
+print(result[2])
+printTree(queue)
+
+
+
+
+
+
+
+# Iterative Approach is yet to implement.
\ No newline at end of file