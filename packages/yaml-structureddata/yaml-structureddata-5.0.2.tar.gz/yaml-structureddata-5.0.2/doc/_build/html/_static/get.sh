#!/bin/sh

# load the "cerulian" theme from the bootswatch site:

rm -f bootstrap.css
wget http://bootswatch.com/cerulean/bootstrap.css
patch -b -p0 < PATCH 
