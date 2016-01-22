Installations required: Selenium, chromedriver

Steps:
1. Enter your LinkedIn login credentials in lines 16 and 17 under user_name and password.
2. Make sure there is a 'Csvs' folder and a 'Dicts' folder in your current working directory(P1).
3. Find your LinkedIn profile ID and change it in the start_id variable.
4. Run: python p1.py

Output:
1. edge_list.csv, containing the list of edges separated by newline.
2. edge_count.csv, containing the number of endorsements for each node.
3. anon_map.csv, containing the mapping for each name with a number, assigned according to the order in which the nodes were visited in BFS, starting from 1.
4. anon_edge_list.csv, containing the anonymized edge list based on the anon_map.
5. The set of dictionaries from which the above csv files were generated, present in the Dicts folder inside P1.



