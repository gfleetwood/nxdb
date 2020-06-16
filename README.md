# NXDB

Sqlite tested but ultimately database agnostic functions for storing networkx graphs.

* nx_to_db: Node oriented version of networkx's edge oriented to_pandas_dataframe()

* nx_from_db: Node oriented version of networkx's edge oriented from_pandas_dataframe()

There are a number of ways to improve the code leverage networkx functions instead of custom python code.

* Use add_nodes_from to add multiple nodes.
