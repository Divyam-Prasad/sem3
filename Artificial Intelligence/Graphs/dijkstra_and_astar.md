# Dijkstra's Algorithm and A* Search

## 1. The Intuition, Building on BFS

Recall from the graph traversal doc: **BFS finds the shortest path in an unweighted graph** by expanding outward layer by layer, one edge at a time. That works because in an unweighted graph, "fewest edges" *is* "shortest path."

But real-world graphs usually have **weighted edges** — a road between two cities isn't the same "cost" as a road between two neighboring houses. Plain BFS breaks here: it would treat a 1km road and a 500km highway as equally costly, since it only counts hops.

**Dijkstra's algorithm** fixes this. Instead of a plain queue (FIFO), it uses a **priority queue** ordered by *total distance traveled so far*, always expanding the currently-cheapest-to-reach node next. It's the algorithm underneath the "shortest route" feature in a GPS app when you're optimizing purely for distance/time, with no awareness of which direction the destination actually is.

**A\*** takes Dijkstra and adds one more idea: if you *know roughly where the destination is* (e.g., its straight-line distance), why waste time exploring nodes that are clearly moving away from it? A* uses that hint — a **heuristic** — to prioritize promising directions, so it explores far fewer nodes in practice while still guaranteeing the shortest path (under conditions we'll cover).

---

## 2. Dijkstra's Algorithm

### Mechanics

1. Maintain a `dist` map: best known distance from the source to every node (start at infinity, except source = 0).
2. Maintain a min-heap (priority queue) of `(distance, node)`, seeded with `(0, source)`.
3. Pop the cheapest `(distance, node)`. If we've already finalized this node with a better distance, skip it (handles stale heap entries).
4. For each neighbor, check if going through the current node offers a **shorter** path than what's currently recorded ("relaxation"). If so, update it and push the new distance onto the heap.
5. Repeat until the heap is empty (or until you pop your target, if you only care about one destination).

```python
import heapq

def dijkstra(graph, source):
    """
    graph: dict of dict, e.g. {'A': {'B': 4, 'C': 1}, 'B': {'D': 1}, ...}
           meaning edge A->B has weight 4, A->C has weight 1
    Returns: dict of shortest distance from source to every reachable node
    """
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    pq = [(0, source)]          # (distance_so_far, node)
    visited = set()

    while pq:
        d, node = heapq.heappop(pq)

        if node in visited:
            continue             # stale entry — we already finalized this node cheaper
        visited.add(node)

        for neighbor, weight in graph[node].items():
            new_dist = d + weight
            if new_dist < dist[neighbor]:      # relaxation step
                dist[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return dist
```

**Reconstructing the actual path** (not just the distance) — track where each node's best distance came from:

```python
def dijkstra_with_path(graph, source, target):
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    prev = {node: None for node in graph}
    pq = [(0, source)]
    visited = set()

    while pq:
        d, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if node == target:
            break                 # early exit once we've finalized the target

        for neighbor, weight in graph[node].items():
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))

    # walk backwards from target to source
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path, dist[target]
```

### Why "greedy" works here

Dijkstra is a **greedy algorithm**: once it pops a node from the priority queue, it never revisits or reconsiders that node's finalized distance. This greedy choice is only *provably correct* because of one requirement: **all edge weights must be non-negative**. If a negative edge existed, a path you already "finalized" as optimal could later become beatable by a longer path that eventually hits a negative edge — greedy can't see that coming. (That's exactly what **Bellman-Ford** exists for — it handles negative weights by relaxing all edges repeatedly, at the cost of O(V·E) instead of O((V+E) log V).)

### Complexity

With a binary heap: **O((V + E) log V)** — each node is popped once (log V per pop), and each edge can trigger one push (log V per push).

### Real scenario

Google/Apple Maps computing "fastest route" when optimizing purely on road segment weights (distance or predicted time) is conceptually Dijkstra (in practice they use heavily optimized variants like Contraction Hierarchies, but Dijkstra is the base idea). Network routers use Dijkstra-family algorithms (OSPF — Open Shortest Path First) to compute the cheapest path for packets across a network.

---

## 3. A* Search

### The one new idea: a heuristic

A* is Dijkstra plus a **heuristic function `h(n)`**: an *estimate* of the remaining distance from node `n` to the goal. Instead of prioritizing purely by "distance traveled so far" (`g(n)`, exactly what Dijkstra uses), A* prioritizes by:

```
f(n) = g(n) + h(n)
       ^         ^
  cost so far   estimated cost to go
  (known,        (guessed, using domain
   exact)         knowledge)
```

Think of Dijkstra as exploring in **all directions equally**, like ripples spreading from a stone dropped in water. A* **biases the ripple** toward the goal, like ripples spreading faster on the side facing the target — because `h(n)` keeps nudging the priority queue to prefer nodes that *look* closer to the destination.

**Common heuristics** (for grid/map-like problems):
- **Euclidean distance** (`sqrt(dx² + dy²)`) — if you can move in any direction.
- **Manhattan distance** (`|dx| + |dy|`) — if you can only move in 4 directions (grid, like a city block map).
- **Chebyshev distance** (`max(|dx|, |dy|)`) — if diagonal movement costs the same as straight movement (8-directional grid, like a chess king).

### Code

```python
import heapq

def heuristic(a, b):
    # Euclidean distance between two (x, y) coordinates
    (x1, y1), (x2, y2) = a, b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def a_star(graph, coords, source, target):
    """
    graph: dict of dict, e.g. {'A': {'B': 4}, ...} — same as Dijkstra
    coords: dict mapping node -> (x, y), used by the heuristic
    """
    g_score = {node: float('inf') for node in graph}
    g_score[source] = 0
    prev = {node: None for node in graph}

    # priority queue ordered by f(n) = g(n) + h(n)
    pq = [(heuristic(coords[source], coords[target]), source)]
    visited = set()

    while pq:
        _, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if node == target:
            break

        for neighbor, weight in graph[node].items():
            tentative_g = g_score[node] + weight
            if tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                prev[neighbor] = node
                f_score = tentative_g + heuristic(coords[neighbor], coords[target])
                heapq.heappush(pq, (f_score, neighbor))

    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path, g_score[target]
```

Notice how structurally similar this is to `dijkstra_with_path` — the **only** difference is the priority queue key: Dijkstra pushes `new_dist`, A* pushes `new_dist + heuristic(...)`. That's the entire algorithmic delta. Everything else (relaxation, visited set, path reconstruction) is identical.

### The guarantee: admissibility

A* is only guaranteed to find the *truly* shortest path if the heuristic is **admissible** — it must **never overestimate** the true remaining cost. Euclidean distance is admissible on a map where you can't move faster than "as the crow flies" — the real road distance is always ≥ straight-line distance, so the heuristic never lies optimistically.

If your heuristic *overestimates* (say, you used a heuristic based on real-world traffic that assumes worse conditions than reality), A* can lock in a suboptimal path early because it undervalues a route that's actually better. If `h(n) = 0` everywhere, A* **degrades exactly into Dijkstra** — no bias at all, since `f(n) = g(n) + 0`.

### Complexity

Worst case is the same as Dijkstra, **O((V + E) log V)**, since a bad/zero heuristic makes A* explore just as much as Dijkstra. But with a **good** heuristic, A* explores dramatically fewer nodes in practice — this is where the real-world speedup comes from, not from a better asymptotic bound.

### Real scenario

**Video game pathfinding** is the canonical A* use case — an NPC navigating a map toward the player uses grid coordinates for a cheap, admissible heuristic (Manhattan/Euclidean/Chebyshev depending on allowed movement), so it doesn't waste cycles exploring the entire map like Dijkstra would. It's also used in **puzzle solvers** (like the 15-puzzle or Rubik's Cube solvers), where `h(n)` might be "number of misplaced tiles" — a cheap-to-compute admissible estimate of how far a state is from being solved.

---

## 4. Comparison Table

| | BFS | Dijkstra | A* |
|---|---|---|---|
| Handles weighted edges? | No (assumes all edges cost 1) | Yes | Yes |
| Handles negative weights? | N/A | No (use Bellman-Ford) | No |
| Uses a heuristic? | No | No | Yes — `h(n)` |
| Priority queue ordered by | N/A (plain FIFO queue) | `g(n)` — cost so far | `f(n) = g(n) + h(n)` |
| Explores | Uniformly outward, by hop count | Uniformly outward, by cost | Biased toward the goal |
| Worst-case complexity | O(V + E) | O((V + E) log V) | O((V + E) log V) |
| Practical nodes explored | Fewest (unweighted case) | More than A* on same problem | Fewest, if heuristic is good |
| Guarantees shortest path? | Yes (unweighted only) | Yes (non-negative weights) | Yes, **if heuristic is admissible** |

## 5. Interview Gotchas

- **"Why not just use BFS with weighted edges?"** — Because BFS's FIFO queue has no concept of "cheaper," it would finalize a node the first time it's *reached*, not the first time it's reached *cheaply*. A path with more hops but lower total weight would get ignored. That's the exact gap Dijkstra's priority queue closes.
- **Forgetting the "stale entry" check** (`if node in visited: continue`) — since you can push the same node multiple times as shorter paths are discovered, without this check you'd process outdated distances and potentially re-relax with worse values.
- **Using A* with an inadmissible heuristic** and being surprised the path isn't actually shortest — always double check `h(n)` never overestimates true cost.
- **Negative weights** — neither Dijkstra nor A* handle them correctly. That's a hard signal in an interview to pivot to Bellman-Ford (or Johnson's algorithm if you need all-pairs shortest paths with negative edges but no negative cycles).
