# Caching-Proxy
 Created caching proxy cli tool which takes an origin from user and caches stuff from that origin.

# Main aims:
-Bare bones app with minimal code for ease of implementation (so practicality may be overlooked in some places)

-Want a clear and concise understanding of caching and proxy caching

-Want to learn about cli tools in python via argsparse

-Want to get an understanding of http servers which will be used in http caching for this proxy

# How to run (example):
-->Install dependencies:

pip install -r requirements.txt

-->Run app:

python app.py --port 3000 --origin http://dummyjson.com

-->Open browser and make a request:

http://localhost:3000/products

-->Repeat and see Cache Hits and Misses in terminal

\
\
-->Clear Cache:

python app.py --clear-cache

# Inspiration:
https://roadmap.sh/projects/caching-server

