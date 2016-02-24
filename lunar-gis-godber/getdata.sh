#!/usr/bin/env bash

# These products and related products can be found at:
#   http://wms.lroc.asu.edu/lroc/rdr_product_select
# NOTE: These are not necessarily the highest resolution products available

# http://wms.lroc.asu.edu/lroc/view_rdr_product/WAC_GLOBAL_P900S0000_128P
wget -nc http://lroc.sese.asu.edu/data/LRO-L-LROC-5-RDR-V1.0/LROLRC_2001/DATA/SDP/WAC_GLD100/WAC_GLD100_P900S0000_128P.IMG
# http://wms.lroc.asu.edu/lroc/view_rdr_product/WAC_GLD100_P900S0000_128P
wget -nc http://lroc.sese.asu.edu/data/LRO-L-LROC-5-RDR-V1.0/LROLRC_2001/DATA/BDR/WAC_GLOBAL/WAC_GLOBAL_P900S0000_128P.IMG

# Zip file containing shp, dbf, shx and prj files for lunar global mare boundaries - (5.53 MB)
# http://wms.lroc.asu.edu/lroc/view_rdr/SHAPEFILE_LUNAR_MARE
wget -nc http://lroc.sese.asu.edu/data/LRO-L-LROC-5-RDR-V1.0/LROLRC_2001/EXTRAS/SHAPEFILE/LUNAR_MARE/LROC_GLOBAL_MARE.ZIP
mkdir -p global_mare
cd global_mare
unzip -u ../LROC_GLOBAL_MARE.ZIP
