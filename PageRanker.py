
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



def calculate_page_rank (beta=0.85, dleta=0.001, maxIterations=20):
    pass

def get_PageRank(node_name):
    pass

def get_top_nodes(n):
    pass


def get_all_PageRank():
    pass

load_graph("C:\\Users\\Giz\\Desktop\\Wikipedia_votes.csv")