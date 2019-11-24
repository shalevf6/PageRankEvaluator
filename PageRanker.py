from __future__ import with_statement
import csv
import pandas as pd
from pip._vendor.distlib.compat import raw_input
from Node import Node
from itertools import islice


edge_df = None
result_df = None
node_dictionary = {}
number_of_nodes = 0


def load_graph(path):
    global edge_df
    global node_dictionary
    global number_of_nodes
    try:
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            edge_df = pd.DataFrame(csv_reader,columns=['source','destination'])
            i = 0
            # go through all the nodes and add them to the dictionary
            for index, record in edge_df.iterrows():
                source_node = record[0]
                destination_node = record[1]

                if source_node not in node_dictionary.keys():
                    new_node = Node(source_node, set(), set())
                    node_dictionary[source_node] = new_node
                node_dictionary[source_node].add_outgoing_node(destination_node)

                if destination_node not in node_dictionary.keys():
                    new_node = Node(destination_node, set(), set())
                    node_dictionary[destination_node] = new_node
                node_dictionary[destination_node].add_incoming_node(source_node)
            number_of_nodes = len(node_dictionary.keys())
    except EnvironmentError:
        print("directory or file not exists")


# updates the PageRank for the current iteration
# beta - the beta element in the PageRank formula
# first_iteration - a boolean element for initializing the PageRank formula
def update_pagerank(beta, first_iteration):
    global result_df
    global node_dictionary
    global number_of_nodes
    # in the first iteration, the pagerank of all nodes is 1 / N
    if first_iteration is True:
        first_pagerank_value = float(1) / float(number_of_nodes)
        for name, node in node_dictionary.items():
            node.set_pagerank(first_pagerank_value)
    else:
        # transfer all current pagerank values to be previous pagerank values
        for name, node in node_dictionary.items():
            node.set_curr_to_prev()

        # from the formula - S
        s = 0
        for name, node in node_dictionary.items():
            # from the formula - r'j(t)
            temporary_pagerank_value = 0
            incoming_nodes = node.get_incoming_nodes()
            # iterate through all the incoming nodes
            for incoming_node_name in incoming_nodes:
                incoming_node = node_dictionary[incoming_node_name]
                # from the formula - di
                out_degree = incoming_node.get_out_degree()
                # from the formula - ri(t-1)
                prev_pagerank_value = incoming_node.get_pagerank(True)
                # from the formula - sigma on -> beta * (ri(t-1)/di)
                temporary_pagerank_value = temporary_pagerank_value + float(beta * (prev_pagerank_value / out_degree))
            # accumulate in order to get S's value
            s = s + temporary_pagerank_value
            # temporarily update the node's pagerank value to be the temporary pagerank values
            node.set_temp_pagerank(temporary_pagerank_value)

        # update the new pagerank value for all the nodes
        # from the fromula - ((1-S)/N)
        leaked_pagerank = float(1-s) / float(number_of_nodes)
        for name, node in node_dictionary.items():
            temporary_pagerank_value = node.get_temp_pagerank()
            # calculate the pagerank value from the formula - r'j(t) + ((1-S)/N)
            new_pagerank_value = temporary_pagerank_value + leaked_pagerank
            # insert new pagerank value into the result dataframe
            node.set_pagerank(new_pagerank_value)


# checks if the current conditions of the PageRank calculations apply with the given delta
# delta - the delta element in the PageRank formula
def check_if_conditions_apply(delta):
    total_score = 0
    for name, node in node_dictionary.items():
        prev_pagerank = node.get_pagerank(True)
        curr_pagerank = node.get_pagerank(False)
        total_score = total_score + abs(prev_pagerank - curr_pagerank)
    if total_score > delta:
        return True
    else:
        return False


# creates the final sorted results dataframe from all the nodes in the dictionary
def get_final_dataframe():
    global node_dictionary
    df = pd.DataFrame(columns=['node_name', 'page_rank_value'])
    for name, node in node_dictionary.items():
        new_row = [name, node.get_pagerank(False)]
        df.loc[len(df)] = new_row
    df = df.sort_values(by=['page_rank_value'], ascending=False)
    return df


# checks if a given number is an integer
# number - a given number
def check_if_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False


# checks if a given number is an integer
# number - a given number
def check_if_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False


# calculates the page rank for the loaded graph
# beta, delta - the beta and delta elements in the PageRank formula
# max_iterations - the maximum number of iterations for the algorithm
def calculate_page_rank (beta=0.85, delta=0.001, max_iterations=20):

    # check if all the parameters are ok
    if check_if_float(beta) is False or check_if_float(delta) is False or check_if_int(max_iterations) is False:
        print("one or more of the parameters inserted is incorrect")
        return

    global result_df
    global node_dictionary

    # updates the initial PageRank values
    update_pagerank(beta, True)

    # updates the result to be the first iteration in case the max_iterations parameter is 0
    if max_iterations == 0:
        result_df = get_final_dataframe()
    else:

        # updates the PageRank values of the first iteration
        update_pagerank(beta, False)
        curr_iter = 1

        # checks whether the delta is valid
        passed = check_if_conditions_apply(delta)

        # iterates over the PageRank algorithm
        while curr_iter <= max_iterations and passed:
            curr_iter = curr_iter + 1

            # updates the PageRank values for this iteration
            update_pagerank(beta, False)

            # checks whether the delta is valid
            passed = check_if_conditions_apply(delta)

        result_df = get_final_dataframe()



# gets the page rank of a specific node
def get_PageRank(node_name):
    global node_dictionary
    if node_name in node_dictionary.keys():
        return node_dictionary[node_name].get_pagerank(False)
    return -1


# gets a list of n nodes with the highest page rank
def get_top_nodes(n):
    ans = []
    if result_df is None or edge_df is None or not n.isdigit():
        return ans
    for index, record in islice(result_df.iterrows(),int(n)):
        ans.append([int(record[0]),float(record[1])])
    return ans


# gets a list of the page rank of all the nodes
def get_all_PageRank():
    ans = []
    if result_df is None or edge_df is None:
        return ans
    for index, record in result_df.iterrows():
        ans.append([int(record[0]),float(record[1])])
    return ans
