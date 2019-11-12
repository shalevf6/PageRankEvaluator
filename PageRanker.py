
import csv
import pandas as pd
import numpy as np

edge_df = None
result_df = None


def load_graph(path):
    global edge_df
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        edge_df = pd.DataFrame(csv_reader)


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
    pass


def get_top_nodes(n):
    pass


def get_all_PageRank():
    pass

load_graph("C:\\Users\\Shalev\\Desktop\\Wikipedia_votes.csv")
incoming_node_list = edge_df.loc[edge_df[1] == '28']
print(incoming_node_list)

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