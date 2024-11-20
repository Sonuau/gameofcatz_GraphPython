import random

class Vertex(object):

    def __init__(self, key, index, payload=None):
        self.key = key
        self.payload = payload
        self.index = index

    def __str__(self):
        return self.key

    def __repr__(self):
        return str(self)


class Graph(object):
    def __init__(self, max_vertices=100):
        self.matrix = [[None] * max_vertices for _ in range(max_vertices)]  # 2d array (list of lists)
        self.num_vertices = 0  # current number of vertices
        self.vertices = {}  # vertex dict
        self.i_to_key = []  # list of keys to look up from index
        self.numOfEdges = 0

    def add_vertex(self, key, payload=None):
        """ add vertex named key if it is not already in graph"""
        assert self.num_vertices < len(self.matrix), "max vertices reached,  can not add more!"
        if key not in self.vertices:
            self.i_to_key.append(key)
            i = self.num_vertices
            self.vertices[key] = Vertex(key, i, payload)
            self.num_vertices = i + 1

    def get_vertex(self, key):
        return self.vertices[key]

    def update_vertex(self, new_key, old_key):
        self.i_to_key[self.vertices[old_key].index] = new_key
        self.vertices[old_key] = Vertex(new_key, self.num_vertices, None)

    def add_edge(self, from_key, to_key, weight=None):
        """ create vertices if needed and then set weight into matrix"""
        self.add_vertex(from_key)
        self.add_vertex(to_key)
        self.matrix[self.vertices[from_key].index][self.vertices[to_key].index] = weight
        self.numOfEdges = self.numOfEdges+1

    def update_edge(self,s,d,w):
        self.matrix[self.vertices[s].index][self.vertices[d].index] = w

    def delete_edge(self, s, d, w):
        self.matrix[self.vertices[s].index][self.vertices[d].index] = w

    # func1
    def parameter_tweaks(self):
        for i in range(50):
            v1 = self.i_to_key[random.randint(0, self.num_vertices-1)]
            v2 = self.i_to_key[random.randint(0, self.num_vertices-1)]
            possible_weights = [0,100,-1,1]
            w = random.randint(0,3)
            self.add_edge(v1,v2,possible_weights[w])
        print("50 Tweak parameters being passed")
        # tweaks = []
        # for i in range(self.numOfEdges):
        #     ran = random.randint(0, 3)
        #     tweaks.append(possible_weights[ran])
        # print(tweaks)
        # i = 0
        # for v1 in self.vertices:
        #     v2 = self.edges(v1)
        #     print(v1,self.edges(v1))
        #     for x in v2:
        #         if len(x)>0:
        #             print(x)
        #             self.update_edge(v1,x[0],tweaks[i])
        #             i = i+1

    def delete_node(self,v):
        remove_key = self.vertices.pop(v, None)
        if remove_key != None:
            print(v,"has been removed ")
            i = self.num_vertices
            self.num_vertices = i-1
            self.i_to_key.remove(v)
        else:
            print(v,"Not found")

    def get_vertices(self):
        """returns the list of all vertices in the graph."""
        return self.vertices.values()

    def __contains__(self, key):
        return key in self.vertices

    def edges(self, from_key):
        """ return list of tuples (to_vertex, weight) of all edges from vertex_key key"""
        to_dim = self.matrix[self.vertices[from_key].index]
        return [(g.vertices[g.i_to_key[i]], w) for i, w in enumerate(to_dim) if w]

    # func2
    def display_graph(self):
        print("Displaying Graph:")
        print(" ", "  ".join([v.key for v in g.get_vertices()]))
        for i in range(g.num_vertices):
            row = map(lambda x: str(x) if x else '0' , g.matrix[i][:g.num_vertices])
            print(g.i_to_key[i], "  ".join(row))
        ch = int(input("Do you want to save this graph (1/0)"))
        if ch == 1:
            with open("graph_output.txt", 'w', encoding='utf-8') as f:
                f.write(" ")
                f.write("  ".join([v.key for v in g.get_vertices()]))
                f.write("\n")
                for i in range(g.num_vertices):
                    row = map(lambda x: str(x) if x else '0', g.matrix[i][:g.num_vertices])
                    f.write(g.i_to_key[i])
                    f.write("  ".join(row))
                    f.write("\n")

    # func3
    def value(self,x):
        if x == 0 :
            x = '-'
        elif x == -1:
            x = "Food"
        elif x == 1:
            x = 'Toy'
        elif x == 100:
            x = 'Dog'
        return x

    def display_world(self):
        print("Displaying World:")
        print(' ',"    ".join([v.key for v in g.get_vertices()]))
        for i in range(g.num_vertices):
            row = map(lambda x: self.value(x) if x else '-', g.matrix[i][:g.num_vertices])
            print(g.i_to_key[i],"    ".join(list(row)))
        ch = int(input("Do you want to save this graph (1/0)"))
        if ch == 1:
            with open("graph_output.txt", 'w', encoding='utf-8') as f:
                f.write(" ")
                f.write("  ".join([v.key for v in g.get_vertices()]))
                f.write("\n")
                for i in range(g.num_vertices):
                    row = map(lambda x: self.value(x) if x else '0', g.matrix[i][:g.num_vertices])
                    f.write(g.i_to_key[i])
                    f.write("  ".join(row))
                    f.write("\n")

    def generate_route(self):
        destination_vertex = self.i_to_key[self.num_vertices-1]
        route = []
        route.append('A')
        for i in range(50):
            v2 = self.i_to_key[random.randint(0, self.num_vertices-1)]
            if v2 not in route:
                route.append(v2)
            if v2 == destination_vertex:
                break
        i = 0
        while i < len(route)-1:
            self.add_edge(route[i],route[i+1],1)
            i = i + 1
        print("A route from source to destination has been generated")
        print(route)

    def display_route(self):
        route = []
        route.append('A')
        i = 0
        v = self.i_to_key[0]
        while i < self.num_vertices:
            e = self.edges(v)
            for x in e:
                if len(x)>0:
                    # print(v,x[0],x[1])
                    if x[1] == 1:
                        route.append(x[0])
                        v = str(x[0])
                        break
            i = i+1
        last = str(route[len(route)-1])
        if last != 'J':
            print('No route matches the destination')
        else:
            print("Possible route from 'A' to 'J' is : ",route)
            ch = int(input("Do you want to save this route ? 1/0"))
            if ch == 1:
                with open("route.txt", 'w', encoding='utf-8') as f:
                    f.write(route)

    def save_to_file(self):
        with open("graph_output.txt", 'w', encoding='utf-8') as f:
            f.write(" ")
            f.write("  ".join([v.key for v in g.get_vertices()]))
            f.write("\n")
            for i in range(g.num_vertices):
                row = map(lambda x: str(x) if x else '0', g.matrix[i][:g.num_vertices])
                f.write(g.i_to_key[i])
                f.write("  ".join(row))
                f.write("\n")

# func4
#    def generate_routes(self, from_key, to_key):


if __name__ == '__main__':
    g = Graph()
    while(True):
        print('''1-Load Input file
2-Node operations
3-Edge operations
4-Parameter Tweaks
5-Display Graph
6-Display Word
7-Generate Route
8-Display Routes
9-Save network
        ''')
        ch = int(input("Enter choice : "))
        if ch==1:
            file = open('graph.txt')
            for line in file:
                v1 = line[0]
                v2 = line[2]
                w = line[4]
                if w == '-':
                    w = 0
                elif w == 'F':
                    w = -1
                elif w == 'T':
                    w = 1
                elif w == 'D':
                    w = 100
                g.add_edge(v1, v2, w)
            print('File has been read and graph has been created !')
        if ch==2:
            print('''1-Add
2-Delete
3-Find
4-Update''')
            ch2 = int(input('Choose : '))
            if ch2 == 1:
                v = input('Enter vertex name : ')
                g.add_vertex(v)
            if ch2 == 2:
                v = input('Enter vertex name : ')
                g.delete_node(v)
            if ch2 == 3:
                v = input('Enter vertex name : ')
                print(v," in graph (True/False) : ", v in g)
            if ch2 == 4:
                vO = input('Enter old vertex name : ')
                vN = input('Enter new vertex name : ')
                g.update_vertex(vN,vO)
        if ch == 3:
            print("1-Add Edge\n"
                  "2-Remove Edge\n"
                  "3-Find Edge\n"
                  "4-Update Edge\n")
            ch2 = int(input("Choose:"))
            if ch2 == 1:
                v1 = int(input("Enter vertex 1 :"))
                v2 = int(input("Enter vertex 2 :"))
                w = int(input("Enter weight (-1,0,1,100):"))
                g.add_edge(v1,v2,w)
            if ch2 == 2:
                v1 = int(input("Enter vertex 1 for the edge to remove :"))
                v2 = int(input("Enter vertex 2 for the edge to remove :"))
                g.delete_edge(v1,v2,0)
                print("Edge between",v1,v2,"Has been removed")
            if ch2 == 4:
                v1 = int(input("Enter vertex 1 for the edge to update :"))
                v2 = int(input("Enter vertex 2 for the edge to update :"))
                w = int(input("Enter weight for the edge to update :"))
                g.update_edge(v1,v2,w)
                print(v1,"-",v2," is Updated to weight ",w)
            if ch2 == 3:
                v = int(input("Enter vertex to find it's edges:"))
                print(g.edges(v))
        if ch == 4:
            g.parameter_tweaks()
        if ch == 5:
            g.display_graph()
        if ch == 6:
            g.display_world()
        if ch == 7:
            g.generate_route()
        if ch == 8:
            g.display_route()
        if ch == 9:
            g.save_to_file()
