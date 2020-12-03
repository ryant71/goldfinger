Goldfinger
==========

Aim
---

Build a site based on Dash which graphs metals prices.

Purpose
-------

1. Get the site working for limited use by one or two people
2. Implement it in such a way that I learn lots of new
things as I go.


Initial Goal
------------

Get data via the API at metals-api.com.

Graph:

Gold = XAU
Silver = XAG

In:

South African Rand = ZAR
United States Dollar = USD

Example Response
```
{
   "date" : "2020-09-26",
   "success" : true,
   "base" : "USD",
   "timestamp" : 1601130120,
   "unit" : "per ounce",
   "rates" : {
      "XPT" : 0.001173616515,
      "USD" : 1,
      "XAU" : 0.00053724702,
      "XAG" : 0.04367511366,
      "XPD" : 0.000450828378,
      "XRH" : 7.2463768115942e-05
   }
}
```

This will be cached in Redis because metals-api.com API calls
have a monthly limit.


Parts
-----

* Redis docker
* Dash docker
* Metals-api script to fetch and store data
* Helpers

TODO
----

1. Make Makefile work with docker-compose and for standalone parts
2. Make it deployable in some basic way
   i. Just scp and ssh at first
   ii. Salt later?
3. Make app.py fetch from Redis at some predermined interval
   i. Maybe it'll have to use async of some sort
4. Make it deployable via CircleCI
   i. beta and prod targets
5. Add functionality for user to add purchases and store that data somewhere
   i. Same interface as Dash or another page?
   ii. Redis?
6. Graph the total purchases over time
