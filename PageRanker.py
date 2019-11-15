
import csv
import pandas as pd
from pip._vendor.distlib.compat import raw_input
from Node import Node

edge_df = None
result_df = None
node_dictionary = {}
number_of_nodes = 0


def load_graph(path):
    global edge_df
    global node_dictionary
    global number_of_nodes
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        edge_df = pd.DataFrame(csv_reader,columns=['source','destination'])

        idx = 0
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
            print(idx)
            idx = idx + 1

        number_of_nodes = len(node_dictionary.keys())


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
        idx = 0
        for name, node in node_dictionary.items():
            print(idx)
            idx = idx + 1
            node.set_pagerank(first_pagerank_value)
    else:
        # from the formula - S
        s = 0
        idx = 1
        for name, node in node_dictionary.items():
            print(idx)
            idx = idx + 1
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
    if total_score <= delta:
        return False
    else:
        return True


# creates the final sorted results dataframe from all the nodes in the dictionary
# previous - True if the results should be the last iteration's results, else - False
def get_final_dataframe(previous):
    global node_dictionary
    df = pd.DataFrame(columns=['node_name', 'page_rank_value'])
    for name, node in node_dictionary.items():
        if previous:
            node.set_prev_to_cur()
        new_row = [name, node.get_pagerank(False)]
        df.loc[len(df)] = new_row
    df = df.sort_values(by=['page_rank_value'], ascending=False)
    return df


# calculates the page rank for the loaded graph
# beta, delta - the beta and delta elements in the PageRank formula
# max_iterations - the maximum number of iterations for the algorithm
def calculate_page_rank (beta=0.85, delta=0.001, max_iterations=20):
    global result_df
    global node_dictionary
    curr_iter = 0

    # updates the PageRank values for the first iteration
    update_pagerank(beta, True)

    # updates the result to be the first iteration in case the max_iterations parameter is 0
    if max_iterations == 0:
        result_df = get_final_dataframe(False)
    else:
        # iterates over the PageRank algorithm
        delta_was_valid = False
        while curr_iter <= max_iterations:
            curr_iter = curr_iter + 1

            # updates the PageRank values for this iteration
            update_pagerank(beta, False)

            # checks whether the delta is valid
            if curr_iter > 1:
                passed = check_if_conditions_apply(delta)
                if not passed:
                    result_df = get_final_dataframe(True)
                    delta_was_valid = True
                    break

        if not delta_was_valid:
            result_df = get_final_dataframe(False)


# gets the page rank of a specific node
def get_PageRank(node_name):
    global node_dictionary
    if node_name in node_dictionary.keys():
        return node_dictionary[node_name].get_pagerank(False)
    return -1


# gets a list of n nodes with the highest page rank
def get_top_nodes(n):
    ans = []
    if result_df is None or edge_df is None:
        return ans
    for index, record in result_df.iterrows():
        ans.append(int(record[0]))
    return ans


# gets a list of the page rank of all the nodes
def get_all_PageRank():
    ans = []
    if result_df is None or edge_df is None:
        return ans
    for index, record in result_df.iterrows():
        ans.append([int(record[0]),float(record[1])])
    return ans



def getInput():
    menu_operator = raw_input()
    return menu_operator

def showMenu():
    print("to insert path the the graph file press 1 \n"
                              "to calculate page rank press 2\n"
                              "to get page rank of specific node press 3\n"
                              "to get page ranks of top n nodes press 4\n"
                              "to get all page ranks press 5\n"
                              "to exit press 0\n")


def get_path_from_user():
    print("enter a path to the graph file")
    return raw_input()


def get_params_to_calculating():
    print("if want to use default values enter 0 in one of the values")
    print("enter number for beta")
    beta = raw_input()
    print("enter number for delta")
    delta = raw_input()
    print("enter number for max iteration")
    max_iteration = raw_input()
    return beta,delta,max_iteration


def get_node_name():
    print("enter number name")
    return raw_input()


def get_number_of_top_nodoe_to_print():
    print("enter number of top nodes to print")
    return raw_input()


def print_nodes(node_list_to_print):
    for node in node_list_to_print:
        print("node name: " + node[0] + " node rank: " + node[1])


def switch_case(menu_op):
    if menu_op == '1':
        path = get_path_from_user()
        # path = "C:\\Users\\Shalev\\Desktop\\Wikipedia_votes.csv"
        load_graph(path)
        print(edge_df)
        # calculate_page_rank()
    elif menu_op == '2':
        beta,delta,max_iteration = get_params_to_calculating()
        if beta == '0' or delta == '0' or max_iteration == '0':
            calculate_page_rank()
        else:
            calculate_page_rank(beta,delta,max_iteration)
    elif menu_op == '3':
        name = get_node_name()
        rank = get_PageRank(name)
        print(rank)
    elif menu_op == '4':
        number_of_nodes = get_number_of_top_nodoe_to_print()
        node_list_to_print = get_top_nodes(number_of_nodes)
        print_nodes(node_list_to_print)
    elif menu_op == '5':
        all_nodes_list = get_all_PageRank()
        print_nodes(all_nodes_list)
    else:
        print("wrong input")
        
        

def get_new_menu_input():
    print("enter new menu input")
    return raw_input()


# Shalev's tests
# load_graph("C:\\Users\\Shalev\\Desktop\\Wikipedia_votes.csv")
# print(edge_df)
# edge_df_2 = edge_df
# for row in edge_df.itertuples():
#     for row_2 in edge_df_2.itertuples():
#         print(row)
#         print(row_2)
#
# print(edge_df)
# incoming_node_list = edge_df.loc[edge_df['source'] == '28']
# print(incoming_node_list)
# incoming_node_list.at[edge_df['destination']]
# edge_df.at[edge_df.source == '28', ['destination']] = 6
# incoming_node_list = edge_df.loc[edge_df['source'] == '28']
# print(incoming_node_list)
# incoming_node_list.loc[incoming_node_list.source == '28', ['destination']] = '6'
# print(edge_df)
# print(edge_df.loc[edge_df['source'] == '28']['destination'].values[4])
# print(edge_df.loc[edge_df['source'] == '28']['destination'].values[2])
# incoming_node_list = edge_df.loc[edge_df[1] == '28']
# print(incoming_node_list)

# temp_result_df1 = pd.DataFrame(columns=('node_name', 'pagerank_value'))
# print(temp_result_df1)
# row = [30, 20.5]
# temp_result_df1.loc[len(temp_result_df1)] = row
# row = [1,0.6663]
# temp_result_df1.loc[len(temp_result_df1)] = row
# row = [26, 4]
# temp_result_df1.loc[len(temp_result_df1)] = row
# row = [24578, 0.000885]
# temp_result_df1.loc[len(temp_result_df1)] = row
# print(temp_result_df1)
# temp_result_df1 = temp_result_df1.sort_values(by=['pagerank_value'], ascending=True)
# print(temp_result_df1)
# print()
# print()
# temp_result_df1 = temp_result_df1.head(3)
# print(temp_result_df1)
# print()
# print()
# print()
# arr = []
# for index, record in temp_result_df1.iterrows():
#     arr.append(int(record[0]))
#     print (int(record[0]))
#     print()
#     print (arr)
#     print()

showMenu()
input = getInput()
while (input != '0'):
    switch_case(input)
    input = get_new_menu_input()
