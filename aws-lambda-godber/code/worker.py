import os
import rasterio
from tempfile import NamedTemporaryFile
import json
import sys
from rasterio import features

def raster_shape(raster_path):

    if not os.path.exists(raster_path):
        print "File does not exist: %s" % raster_path

    with rasterio.open(raster_path) as src:

        # read the first band and create a binary mask
        arr = src.read(1)
        ndv = src.nodata
        binarray = (arr == ndv).astype('uint8')

        # extract shapes from raster
        shapes = features.shapes(binarray, transform=src.transform)

        # create geojson feature collection
        fc = {
            'type': 'FeatureCollection',
            'features': []}
        for geom, val in shapes:
            if val == 0:  # not nodata, i.e. valid data
                feature = {
                    'type': 'Feature',
                    'properties': {'name': raster_path},
                    'geometry': geom}
                fc['features'].append(feature)

        # Write to file
        with NamedTemporaryFile(suffix=".geojson", delete=False) as temp:
            temp.file.write(json.dumps(fc))

        return temp.name

if __name__ == "__main__":
    in_path = sys.argv[1]
    out_path = raster_shape(in_path)
    print(out_path)
