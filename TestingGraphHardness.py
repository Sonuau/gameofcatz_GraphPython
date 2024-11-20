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

    def delete_edge(self, s, d, w=0):
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

def load_file(g):
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
    return g

if __name__ == '__main__':

    g = Graph()
    print('Testing file load')
    g = load_file(g)
    g.display_graph()

    print('\nTesting graph formation')
    g.display_graph()

    print('\nTesting word formation')
    g.display_world()

    print('\nTesting paremeter tweaks')
    g.parameter_tweaks()
    g.display_graph()

    print('\nTesting route generation')
    g.generate_route()

    print('\nTesting display route')
    g.display_route()

    print('\nTesting file save')
    g.save_to_file()

    print('\nTesting node operations')
    print('Z node added')
    g.add_vertex('Z')
    g.display_graph()

    print('Z' in g)
    print('Replace A with X')
    g.update_vertex('X','A')
    g.display_graph()

    print('Z node removed')
    g.delete_node('Z')
    g.display_graph()

    print('\nTesting edge operations')
    print('A D egde added')
    g.add_edge('A','D',100)
    g.display_graph()

    print('All A egdes are displayed',g.edges('A'))
    print('Update A D edge with weight 0')
    g.update_edge('A','D',0)
    g.display_graph()

    print('A D EDGE removed')
    g.delete_edge('A','D')
    g.display_graph()

