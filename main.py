from functions_max_flow import *

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    imported_data = graph_import("graphs/graph5.txt")
    graph = imported_data[0]
    flow_type = imported_data[1]
    if flow_type == 1:
        print("problème de flot à cout minimal")
    else:
        print("problème de flot maximal") #méthode F-F ou pousser-réétiqueter

    print_graph_to_matrix_of_values(graph)

    if flow_type == 2:  # flot max
        print("\n =========== ford fulkerson ===========\n")
        ff_mat = ford_fulkerson(graph)[1]
        compute_flow_matrix(graph, ff_mat)

