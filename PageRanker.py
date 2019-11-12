
import csv
import pandas as pd


def load_graph(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        dataFrame = pd.DataFrame(csv_reader)




def calculate_page_rank (beta=0.85, dleta=0.001, maxIterations=20):
    pass

def get_PageRank(node_name):
    pass

def get_top_nodes(n):
    pass


def get_all_PageRank():
    pass