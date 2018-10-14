#!/bin/bash

INDEX_DIR=/var/www/dataengineer/search/
SITECONF_DIR=/etc/nginx/sites-available/

mkdir -p $INDEX_DIR
cp index.html $INDEX_DIR
cp nginx_site.conf $SITECONF_DIR

