# UNC Charlotte 
# ITCS 5153 - Applied AI – Spring 2025 
# Lab 2 
# Solving problems using search from the AIMA book’s code 
# Student ID: 801


# Testing
print("Hello, World! Testing. 1. 2. 3. Testing.\n")


# Imports (search.py from the AIMA textbook)
import search


# Test 1 - Tests the performance of various graph search algorithms
print('Test 1 - Comparing graph search algorithms using a simplified map of Romania...')
# Define each route (problem) and header
t1_routes = [
    search.GraphProblem('Arad', 'Bucharest', search.romania_map),
    search.GraphProblem('Oradea', 'Neamt', search.romania_map),
    search.GraphProblem('Q', 'WA', search.australia_map)
]
t1_route_headers = [
    'Searcher', 
    'romania_map(Arad, Bucharest)', 
    'romania_map(Oradea, Neamt)', 
    'australia_map']
# Compare the algorithms
search.compare_searchers(problems=t1_routes, header=t1_route_headers)


# Setup for tests 2:5
def run_search_alg(test_num, beginning, end, alg_type, map_type):
    """
    Runs search algorithm from beginning to end on map_type
    parameters:
        test_num  (str): Identification/Test #
        beginning (str): Starting City
        end       (str): Destination City
        alg_type  (function): Search Algorithm
        map_type  (graph): Map of cities
    """

    # Print headers
    print(f'\nTest {test_num} - Finding a path from {beginning} to {end}...')
    print(f'Using {alg_type.__name__}:')

    # Track stats and run the search algorithm
    stats = search.InstrumentedProblem(search.GraphProblem(beginning, end, map_type))
    test_alg = alg_type(stats)

    # Print stats, cities, and cost
    print(f'Stats: {stats}')
    print(f'Path Followed:\n    {beginning}')
    for place in test_alg.solution():
        print(f'    {place}')
    print(f'Total miles: {test_alg.path_cost}')


# Test 2 - Finding a path from Arad to Lugoj...
run_search_alg('2', 'Arad',    'Lugoj',     search.breadth_first_tree_search, search.romania_map)


# Test 3 - Finding a path from Craiova to Oradea...
run_search_alg('3', 'Craiova', 'Oradea',    search.breadth_first_tree_search, search.romania_map)


# Test 4 - Finding a path from Sibiu to Bucharest...
run_search_alg('4', 'Sibiu',   'Bucharest', search.breadth_first_tree_search, search.romania_map)


# Test 5 - Finding a path from Sibiu to Bucharest...
run_search_alg('5', 'Sibiu',   'Bucharest', search.depth_first_graph_search,   search.romania_map)

print('\n Done!')