import PageRanker as pr

pr.load_graph("C:\\Users\\Shalev\\Desktop\\Wikipedia_votes.csv")
pr.calculate_page_rank()
print(pr.get_top_nodes(10))