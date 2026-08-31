# Trees, Graphs, and Tries — Intuition, Differences, and Core Operations

## 1. The Big Picture (build the intuition first)

Think of it as a hierarchy of restriction:

```
Graph  ⊇  Tree  ⊇  Trie
(most general)   (most specific)
```

- **Graph** — a set of nodes (vertices) connected by edges, with **no rules**. Any node can connect to any other node, in any pattern, even forming loops. Real-life analogy: **a social network**. You can be friends with anyone, friendships can form triangles (cycles), and there's no single "root" person everyone descends from.

- **Tree** — a graph with rules bolted on: it's **connected** (every node reachable from the root), **acyclic** (no loops), and every node has **exactly one parent** (except the root, which has none). Real-life analogy: **a company org chart** or **your computer's file system**. Every folder has exactly one parent folder; you can't have a folder be its own grandparent.

- **Trie** (a.k.a. prefix tree) — a tree with an even more specific rule: each **edge** represents a **character**, and each **path from the root** represents a **string**. Real-life analogy: **the autocomplete on your phone's keyboard**. Typing "c-a-t" walks you down a path; every node you pass through represents a valid prefix so far.

So a tree *is* a graph (a very disciplined one), and a trie *is* a tree (an even more disciplined one, specialized for strings).

## 2. Fundamental Differences

| Property | Graph | Tree | Trie |
|---|---|---|---|
| Cycles allowed? | Yes | No | No |
| Parent count per node | Unrestricted | Exactly 1 (0 for root) | Exactly 1 (0 for root) |
| Must be connected? | No | Yes | Yes |
| Edge count (n nodes) | 0 to n(n−1)/2 | Exactly n−1 | Depends on alphabet size / shared prefixes |
| What a node represents | Any entity | Any entity | A character (a prefix, if you follow the path from root) |
| What an edge represents | Any relationship | Any relationship | "append this character" |
| Root required? | No | Usually | Always (represents empty string "") |
| Real example | Road map, social graph, flight routes | File system, org chart, HTML DOM, BST | Autocomplete, spellcheck, IP routing table (longest prefix match) |

**The one-line mental model:** a tree is what you get when you take a graph and remove every cycle and every "extra parent" until only one path exists between any two nodes. A trie is what you get when you additionally force every edge label to be a single character and every node to be a shared prefix.

---

## 3. Traversal

### 3a. Tree Traversal

Because a tree has no cycles, you never need a "visited" set — you just recurse down and you're guaranteed to terminate.

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# DFS — Preorder (Node -> Left -> Right)
# Use case: cloning a tree, serializing it (prefix notation), or "process before children"
def preorder(root):
    if not root:
        return
    print(root.val)          # visit
    preorder(root.left)
    preorder(root.right)

# DFS — Inorder (Left -> Node -> Right)
# Use case: on a Binary SEARCH Tree, this visits nodes in SORTED order
def inorder(root):
    if not root:
        return
    inorder(root.left)
    print(root.val)          # visit
    inorder(root.right)

# DFS — Postorder (Left -> Right -> Node)
# Use case: safely deleting/freeing a tree (children before parent),
# or evaluating an expression tree (postfix)
def postorder(root):
    if not root:
        return
    postorder(root.left)
    postorder(root.right)
    print(root.val)          # visit

# BFS — Level order (queue-based, not recursive)
# Use case: "print tree level by level", finding shortest path in an unweighted tree
from collections import deque
def level_order(root):
    if not root:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.val)
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
```

**Intuition for picking one:** if the tree represents nested folders and you want to print `parent, then children`, use preorder. If it's a BST and you want sorted output, use inorder. If you're deleting the tree and must free children before the parent, use postorder. If you care about "distance from root" (e.g., closest managers to the CEO), use level-order/BFS.

### 3b. Graph Traversal

Because a graph **can** have cycles, you now **must** track visited nodes or you'll loop forever.

```python
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C']   # notice the cycle: A-B-D-C-A
}

# DFS — recursive, with explicit visited set
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    if node in visited:
        return
    visited.add(node)
    print(node)
    for neighbor in graph[node]:
        dfs(graph, neighbor, visited)

# DFS — iterative, using an explicit stack (avoids recursion limits on huge graphs)
def dfs_iterative(graph, start):
    visited, stack = set(), [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(node)
            stack.extend(n for n in graph[node] if n not in visited)

# BFS — queue-based; gives shortest path in an UNWEIGHTED graph
def bfs(graph, start):
    visited, queue = {start}, deque([start])
    while queue:
        node = queue.popleft()
        print(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**Real scenario:** DFS is what you'd use to detect a circular dependency in a build system (package A depends on B depends on A → deadlock). BFS is what Google Maps effectively does for "fewest number of road segments" on an unweighted graph, or what LinkedIn uses for "degrees of connection" between you and someone else.

### 3c. Trie Traversal

Traversal here usually means "walk down matching a prefix, then DFS from there to collect all words" — exactly what powers autocomplete.

```python
class TrieNode:
    def __init__(self):
        self.children = {}      # char -> TrieNode
        self.is_end_of_word = False

def collect_words(node, prefix, results):
    if node.is_end_of_word:
        results.append(prefix)
    for char, child in node.children.items():
        collect_words(child, prefix + char, results)

def autocomplete(root, prefix):
    node = root
    for char in prefix:
        if char not in node.children:
            return []          # no words with this prefix
        node = node.children[char]
    results = []
    collect_words(node, prefix, results)
    return results
```

---

## 4. Insertion

### 4a. BST Insertion — O(h), where h = height (O(log n) balanced, O(n) worst case skewed)

```python
def insert_bst(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)
    return root
```
Intuition: you're just walking the same "smaller-go-left, bigger-go-right" comparison you'd use in binary search, until you fall off the tree — that empty spot is where the new node goes.

### 4b. Graph Insertion — O(1) amortized for adding a vertex or edge (adjacency list)

```python
def add_vertex(graph, v):
    graph.setdefault(v, [])

def add_edge(graph, u, v, directed=False):
    graph[u].append(v)
    if not directed:
        graph[v].append(u)   # undirected: relationship goes both ways
```
Intuition: unlike a tree, there's no "correct spot" to insert into — you just declare the new relationship exists. That's why graphs are so cheap to grow but expensive to reason about (no guaranteed structure to exploit).

### 4c. Trie Insertion — O(L), where L = length of the word being inserted

```python
def insert_trie(root, word):
    node = root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end_of_word = True
```
Intuition: you walk character by character, and only create a **new** node when the path doesn't already exist — this is exactly why tries are memory-efficient for words sharing prefixes ("car", "care", "cart" all share the "car" path).

---

## 5. Deletion

### 5a. BST Deletion — O(h), three cases (this is the classic interview trap)

```python
def delete_bst(root, val):
    if not root:
        return root
    if val < root.val:
        root.left = delete_bst(root.left, val)
    elif val > root.val:
        root.right = delete_bst(root.right, val)
    else:
        # Case 1: leaf node — just remove it
        if not root.left and not root.right:
            return None
        # Case 2: one child — replace node with that child
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        # Case 3: two children — replace value with the
        # in-order successor (smallest value in the right subtree),
        # then delete that successor from the right subtree
        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = successor.val
        root.right = delete_bst(root.right, successor.val)
    return root
```
The two-children case is the one people fumble in interviews: you can't just delete the node, because that would orphan both subtrees. You borrow the next-largest value (leftmost node of the right subtree) to take its place, then remove the duplicate.

### 5b. Graph Deletion

```python
def remove_edge(graph, u, v, directed=False):
    if v in graph[u]:
        graph[u].remove(v)
    if not directed and u in graph[v]:
        graph[v].remove(u)

def remove_vertex(graph, v):
    graph.pop(v, None)                       # drop the node itself
    for node in graph:
        if v in graph[node]:                 # drop every edge pointing to it
            graph[node].remove(v)
```
Removing a vertex is O(V + E) in the worst case because — unlike a tree, where removing a node only affects its direct parent/children — a node in a graph could be referenced from *anywhere*, so you must scan for dangling references.

### 5c. Trie Deletion — O(L), with backtracking cleanup

```python
def delete_trie(node, word, depth=0):
    if depth == len(word):
        if not node.is_end_of_word:
            return node, False        # word wasn't actually in the trie
        node.is_end_of_word = False
        # tell caller whether this node can be pruned
        return node, len(node.children) == 0

    char = word[depth]
    if char not in node.children:
        return node, False            # word not present

    child, should_delete_child = delete_trie(node.children[char], word, depth + 1)
    if should_delete_child:
        del node.children[char]

    # this node can be pruned too if it has no children left
    # AND it isn't itself the end of some other word
    can_prune = len(node.children) == 0 and not node.is_end_of_word
    return node, can_prune
```
Intuition: you can't just delete nodes along the word's path — other words might depend on those same nodes (deleting "car" shouldn't break "care"). So you unmark `is_end_of_word`, then walk *back up* pruning only the nodes that (a) have no other children and (b) aren't the end of some other word.

---

## 6. Complexity Cheat Sheet

| Operation | Balanced BST | Unbalanced BST (worst) | Graph (adjacency list) | Trie |
|---|---|---|---|---|
| Search | O(log n) | O(n) | O(V + E) | O(L) |
| Insert | O(log n) | O(n) | O(1) | O(L) |
| Delete | O(log n) | O(n) | O(V + E) worst case | O(L) |
| Traversal (all nodes) | O(n) | O(n) | O(V + E) | O(total chars stored) |

*(n = tree nodes, V = graph vertices, E = graph edges, L = string length)*

---

## 7. When You'd Actually Reach for Each One

- **Trees** — anything hierarchical with a single clear parent: file systems, DOM trees, database indexes (B-trees/B+trees under the hood in Postgres/MySQL), decision trees in ML, the call stack of nested function calls.
- **Graphs** — anything with many-to-many relationships or cycles: road networks (Dijkstra/A* for GPS routing), dependency resolution (npm/pip packages, or Makefiles — detecting circular imports is a DFS cycle check), social networks, recommendation engines.
- **Tries** — string-heavy, prefix-driven lookups: autocomplete/typeahead search, spellcheckers, IP routing tables (longest prefix match), T9 predictive text — anywhere you'd otherwise be doing `startswith()` checks across a huge list of strings, since a trie turns that into O(L) instead of O(n·L).

## 8. Common Interview Gotchas

- Forgetting the **visited set** in graph DFS/BFS → infinite loop on a cycle. Trees never need this because they're cycle-free by definition.
- BST deletion's **two-child case** — always grab successor (or predecessor) instead of just unlinking.
- Confusing **tree height vs. balance** — an unbalanced BST degrades to a linked list (O(n) operations), which is why self-balancing variants (AVL, Red-Black) exist.
- In tries, forgetting to **prune unused nodes** after deletion silently bloats memory over time.
