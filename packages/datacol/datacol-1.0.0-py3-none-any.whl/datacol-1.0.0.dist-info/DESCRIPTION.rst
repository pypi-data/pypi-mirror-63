# DataCol
## An extremely lightweight database module for Python 3.8

## Documentation

### help() Function
A simple function that prints a small, barebones tutorial. Takes no parameters.

### NewDB(*file_name*) class
The core of the DataBorealis module. Creates a new database from a .db file referenced in the single parameter.

### query(*val, param*)
Used to search the database. The *val* parameter specifies the type of data you are searching for (name-value pair (nvp) or single value (vlu)), while the *param* parameter is the keyword you are searching for. The name of a name-value pair, or the value of a single value. Returns the value of a name-value pair, or True/False for a value, depending on whether or not the value exists.

### insert(*val, param*)
Used to insert data into the database. Same parameters as the query() function, but the *param* parameter is the data to be inserted.


