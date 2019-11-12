
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





def calculate_page_rank (beta=0.85, dleta=0.001, maxIterations=20):
    pass

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


showMenu()
input = getInput()
while (input != '0'):
    switch_case(input)
    input = get_new_menu_input()