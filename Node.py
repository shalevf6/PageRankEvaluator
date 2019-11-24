# this class represents a node in the graph
# It contains the node's name, its pagerank value and 2 lists that contains the names of all incoming and outgoing nodes


class Node:

    def __init__(self, name, incoming_nodes, outgoing_nodes):
        self.node_name = name
        self.incoming_nodes = incoming_nodes
        self.outgoing_nodes = outgoing_nodes
        self.curr_pagerank = 0
        self.prev_pagerank = 0
        self.temp_pagerank = 0

    def set_pagerank(self, pagerank):
        self.curr_pagerank = pagerank

    def set_temp_pagerank(self, pagerank):
        self.temp_pagerank = pagerank

    def set_curr_to_prev(self):
        self.prev_pagerank = self.curr_pagerank

    def get_pagerank(self, previous):
        if previous:
            return self.prev_pagerank
        return self.curr_pagerank

    def add_incoming_node(self, incoming_node):
        self.incoming_nodes.add(incoming_node)

    def add_outgoing_node(self, outgoing_node):
        self.outgoing_nodes.add(outgoing_node)

    def get_out_degree(self):
        return len(self.outgoing_nodes)

    def get_incoming_nodes(self):
        return self.incoming_nodes

    def get_temp_pagerank(self):
        return self.temp_pagerank