### The task of this exercise is to implement a simpler API in a standalone web application for searching and comapring the compute instances. The application should:
1. Fetch the prices on a nightly basis. This data is publicly available (once a day).
2. Design a database schema to persist the price data locally
3. Expose this data via a JSON API which accepts query parameters to filter. Query parameters, at the bare minimum, should be cloud_type (azure, gcp,aws), location (europe, asia, etc), number of CPUs and amount of RAM in GB.