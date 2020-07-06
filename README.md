# NXDB

## Overview

Proof of concept scaffolding to convert sqlite databases to networkx digraphs and vice versa. At the moment it only deals with preserving node attributes. There are two main functions: 

* nx_to_db: Node oriented version of networkx's edge oriented [to_pandas_dataframe](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.convert_matrix.to_pandas_dataframe.html).

* nx_from_db: Node oriented version of networkx's edge oriented [from_pandas_dataframe](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.convert_matrix.from_pandas_dataframe.html)

## Future

Generally building out the abstractions to support more graphs and leverage networkx functions for the conversion instead of custom python code.

* Add an edge table to store edge attributes. This would do away with the need to store edges in the node attributes table

* Use add_nodes_from to add multiple nodes
