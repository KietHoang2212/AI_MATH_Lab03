from vertex import Vertex
from typing import Any, Text, List

from queue import Queue


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0


    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex

        return newVertex


    def getVertex(self, n):
        return self.vertList[n] if n in self.vertList else None


    def __contains__(self,n):
        return n in self.vertList


    def addEdge(self, f: Any, t: Any, weight: int = 0):
        if f not in self.vertList:
            nv = self.addVertex(f)

        if t not in self.vertList:
            nv = self.addVertex(t)

        self.vertList[f].addNeighbor(self.vertList[t], weight)


    def getVertices(self):
        return self.vertList.keys()


    def __iter__(self):
        return iter(self.vertList.values())


    def bfs(self, start: Vertex):
        start.setDistance(0)
        start.setPred(None)

        vertQueue = Queue()
        vertQueue.put(start)

        while vertQueue.qsize() > 0:
            currentVert = vertQueue.get()

            for nbr in currentVert.getConnections():
                if nbr.getColor() == 'white':
                    nbr.setColor('gray')
                    nbr.setDistance(currentVert.getDistance() + 1)
                    nbr.setPred(currentVert)

                    vertQueue.put(nbr)

            currentVert.setColor('black')


    def dfs(self):
        time = 0

        for aVertex in self:
            aVertex.setColor('white')
            aVertex.setPred(None)

        for aVertex in self:
            if aVertex.getColor() == 'white':
                self.dfsvisit(aVertex, time)
    

    def dfsvisit(self, startVertex, time, is_print=False):
        startVertex.setColor('gray')

        if is_print:
            print(startVertex.getId(), ' ', end='')

        time += 1
        startVertex.setDiscovery(time)

        for nextVertex in startVertex.getConnections():
            if nextVertex.getColor() == 'white':
                nextVertex.setPred(startVertex)
                time = self.dfsvisit(nextVertex, time, is_print)

        startVertex.setColor('black')
        time += 1
        startVertex.setFinish(time)

        return time


    def traverse_dfs(self):
        for vertex in self:
            key = vertex.getId()
            pred = 'None' if vertex.getPred() is None else vertex.getPred().getId()
            discovery = vertex.getDiscovery()
            finish = vertex.getFinish()

            print("key: {}, pred: {}, discovery: {}, finish: {}".format(key, pred, discovery, finish))


    def traverse_bfs(self):
        for vertex in self:
            key = vertex.getId()
            pred = 'None' if vertex.getPred() is None else vertex.getPred().getId()
            distance = vertex.getDistance()

            print("key: {}, pred: {}, distance: {}".format(key, pred, distance))
    
    def get_transpose(self):
        # Get transpose graph
        g_t = Graph()
        
        for key in self.getVertices():
            g_t.addVertex(key)
        
        # reverse edges
        for i in self.getVertices():
            for j in self.getVertex(i).getConnections():
                g_t.addEdge(j.getId(), i)
        
        return g_t
    
    def print_scc(self):
        # Step 1: DFS on the graph G to compute finishing times for each vertex
        self.dfs()

        # Step 2: Get the transpose graph G^T
        g_t = self.get_transpose()

        # Step 3: DFS on the graph G^T (explore each vertex in order of decreasing finishing time)

        # Get desceding order of finishing time
        vert_order = sorted(self.getVertices(), key=lambda x: self.getVertex(x).getFinish(), reverse=True)
        # print(vert_order)

        time = 0
        for v in vert_order:
            if g_t.getVertex(v).getColor() == 'white':
                g_t.dfsvisit(g_t.getVertex(v), time, True)
                print()


def traverse(y: Vertex):
    x = y
    while (x.getPred()):
        print(x.getId())
        x = x.getPred()
    print(x.getId())


if __name__ == '__main__':
    g = Graph()
    for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        g.addVertex(i)
    
    g.addEdge('a', 'b')
    g.addEdge('b', 'c')
    g.addEdge('b', 'e')
    g.addEdge('b', 'f')
    g.addEdge('c', 'd')
    g.addEdge('c', 'g')
    g.addEdge('d', 'c')
    g.addEdge('d', 'h')
    g.addEdge('e', 'a')
    g.addEdge('e', 'f')
    g.addEdge('f', 'g')
    g.addEdge('g', 'f')
    g.addEdge('h', 'd')
    g.addEdge('h', 'g')

    g.print_scc()
