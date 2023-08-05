# Table Renderers

These are basic methods to serialize tables in Python to common file formats.
Each takes the return value from a Django endpoint using rest-framework of the
form {str: {str: []}} and converts it into either a .tgz'd set of .csv files or
a .xlsx with multiple pages.
