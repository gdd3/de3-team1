#!/bin/bash

mkdir data

wget -O data/item_details_full "http://data.cluster-lab.com/data-newprolab-com/project02/item_details_full?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103635Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=eb8d824e55bd0c50c4ea5adcc5a034f19a6bd1d51a0ada17f8ff3e92885e305f"
wget -O data/catalogs.data "http://data.cluster-lab.com/data-newprolab-com/project02/catalogs?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103619Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=a71f86444926896adcb545c9eb18a1417452db9a9587a3aa45d508c43b35ae77"
wget -O data/catalog_path.data "http://data.cluster-lab.com/data-newprolab-com/project02/catalog_path?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103555Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=1614d2c58972e0e4dcc459be3a548d6f31b21a049c7a72175d01d8208c74a24c"
wget -O data/ratings.data "http://data.cluster-lab.com/data-newprolab-com/project02/ratings?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=HI36GTQZKTLEH30CJ443%2F20181013%2F%2Fs3%2Faws4_request&X-Amz-Date=20181013T103652Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=bfa043b8850d639c00764e49d6cd24ed4d0892054ade97552a6061396efe4a35"
