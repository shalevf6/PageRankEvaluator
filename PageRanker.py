
import csv
import pandas as pd
import numpy as np
from pip._vendor.distlib.compat import raw_input

edge_df = None
result_df = None


def load_graph(path):
    global edge_df
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        edge_df = pd.DataFrame(csv_reader,columns=['source','destination'])




# updates the PageRank for the current iteration
# temp_result_df - the dataframe which will contain the PageRank's result
# prev_temp_result_df - the previous PageRank's iteration results
# beta - the beta element in the PageRank formula
# first_iteration - a boolean element for initializing the PageRank formula
def update_pagerank(temp_result_df, prev_temp_result_df, beta, first_iteration):
    # in the first iteration, the pagerank of all nodes is 1 / N
    if first_iteration is True:
        # getting a list of all the unique nodes available
        source_node_list = list(edge_df['source'].unique())
        destination_node_list = list(edge_df['destination'].unique())
        node_list = list(set(source_node_list) | set(destination_node_list))
        num_of_nodes = len(node_list)
        for node in node_list:
            new_entry = [node, 1 / num_of_nodes]
            temp_result_df.loc[len(temp_result_df)] = new_entry
    else:
        # TODO: calculate S here
        node_list = list(temp_result_df['node_name'])
        for node in node_list:
            # from the formula - r'j(t)
            temporary_pagerank_value = 0
            incoming_node_df = edge_df.loc[edge_df['destination'] == node]
            for incomming_node in incoming_node_df:
                outcoming_node_df = edge_df.loc[edge_df['source'] == incomming_node]
                # from the formula - di
                out_degree = len(outcoming_node_df)
                # from the formula - ri(t-1)
                prev_pagerank_value = prev_temp_result_df.loc[prev_temp_result_df['node_name'] == node]
                temporary_pagerank_value = temporary_pagerank_value + beta * (prev_pagerank_value / out_degree)
            # TODO: need to calculate (1-S)/N for current node
            # TODO: need to insert new PageRank value to dataframe


# checks if the current conditions of the PageRank calculations apply with the given delta
# temp_result_df1, temp_result_df2 - the current / previous PageRank iteration
# delta - the delta element in the PageRank formula
def check_if_conditions_apply(temp_result_df1, temp_result_df2, delta):
    pass


# gets the sorted final result for the PageRank algorithm
def get_sorted_result(temp_result_df1, temp_result_df2, curr_iter):
    if curr_iter % 2 == 0:
        return temp_result_df2.sort_values(by=['pagerank_value'], ascending=False)
    else:
        return temp_result_df1.sort_values(by=['pagerank_value'], ascending=False)


# calculates the page rank for the loaded graph
# beta, delta - the beta and delta elements in the PageRank formula
# max_iterations - the maximum number of iterations for the algorithm
def calculate_page_rank (beta=0.85, delta=0.001, max_iterations=20):
    global result_df
    curr_iter = 0
    temp_result_df1 = pd.DataFrame(columns=('node_name', 'pagerank_value'))
    temp_result_df2 = pd.DataFrame(columns=('node_name', 'pagerank_value'))

    # updates the PageRank values for the first iteration
    update_pagerank(temp_result_df1, None, beta, True)

    # updates the result to be the first iteration in case the max_iterations parameter is 0
    if max_iterations == 0:
        result_df = temp_result_df1.sort_values(by=['pagerank_value'], ascending=False)
    else:
        temp_result_df2 = temp_result_df1

        # iterates over the PageRank algorithm
        while curr_iter <= max_iterations:
            curr_iter = curr_iter + 1

            # checks whether the delta is valid
            if curr_iter > 1:
                passed = check_if_conditions_apply(temp_result_df1, temp_result_df2, delta)
                if not passed:
                    result_df = get_sorted_result(temp_result_df1, temp_result_df2, curr_iter)
                    break

            # updates the PageRank values for this iteration
            if curr_iter % 2 == 0:
                update_pagerank(temp_result_df1, temp_result_df2, beta, False)
            else:
                update_pagerank(temp_result_df2, temp_result_df1, beta, False)

        result_df = get_sorted_result(temp_result_df1, temp_result_df2, curr_iter)


def get_PageRank(node_name):
    for row in result_df:
        if row['node_name'] == node_name:
            return row['pagerank_value']
    return -1



def get_top_nodes(n):
    ans = []
    if edge_df is None:
        return ans
    curr_row = 0
    while curr_row < n:
        ans.append(result_df[curr_row])
        curr_row += 1
    return ans


def get_all_PageRank():
    ans = []
    if edge_df is None:
        return ans
    for row in result_df:
        ans.append(row)
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
        load_graph(path)
        print(edge_df)
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
# print(temp_result_df1)
# temp_result_df1 = temp_result_df1.sort_values(by=['pagerank_value'], ascending=False)
# print(temp_result_df1)

showMenu()
input = getInput()
while (input != '0'):
    switch_case(input)
    input = get_new_menu_input()
