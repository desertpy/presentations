import shapely
from shapely import geometry
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon

import numpy as np
import rasterio
import pandas as pd
import geopandas as gpd

import glob
import fiona
import boto3

import rasterio.features
from rasterio.features import rasterize
from rasterio.profiles import DefaultGTiffProfile


def part_the_geojson(bounds, gdf):
    '''
    Reduces a GeoDataFrame to only the Polygons that intersect with the supplied bounds.
    '''
    todrop = []
    for i, row in gdf.iterrows():
        if row.geometry.intersects(bounds) or row.geometry.contains(bounds):
            new_value = row.geometry.intersection(bounds)
            gdf.at[i, 'geometry'] =  new_value
        else:
            todrop.append(i)
    new = gdf.drop(gdf.index[todrop])
    
    return new


def generate_unitcolor_lookup(path_to_desc=''):
    '''
    Creates a Look Up Table (LUT) for the RGB values of geologic units.
    
    path_to_description_file: Local path to description file containing RGB values.
    (https://github.com/azgs/geologic-map-of-arizona/blob/gh-pages/data/DescriptionOfMapUnits.csv)
    '''
    try:
        unitcolor = pd.read_csv(path_to_desc)
    except:
        unitcolor = pd.read_csv('https://raw.githubusercontent.com/azgs/geologic-map-of-arizona/gh-pages/data/DescriptionOfMapUnits.csv')

    unitcolor = unitcolor.loc[:, ['mapunit', 'areafillrgb']]
    unitcolor['R'] = unitcolor.areafillrgb.apply(lambda x: np.int(x.split(';')[0]))
    unitcolor['G'] = unitcolor.areafillrgb.apply(lambda x: np.int(x.split(';')[1]))
    unitcolor['B'] = unitcolor.areafillrgb.apply(lambda x: np.int(x.split(';')[2]))
    unitcolor = unitcolor.loc[:, ['mapunit', 'R', 'G', 'B']]
    unitcolor = unitcolor.set_index('mapunit')
    
    return unitcolor


def build_class_color_dict(path_to_desc=''):
    ''' 
    Creates a dictionary of geologic unit labels mapped to a
    class id integer and PIL RGB color string. For use in Rastervision Experiment file.
    '''
    if path_to_desc:
        unitcolor = generate_unitcolor_lookup(path_to_desc)
    else:
        unitcolor = generate_unitcolor_lookup()

    for i, row in unitcolor.iterrows():
        newval = 'rgb({},{},{})'.format(row.R, row.G, row.B)
        unitcolor.at[i, 'rgb'] =  newval
        
    colordict = unitcolor.drop(columns=['R','G','B'])
    colordict.drop_duplicates(keep='first', inplace=True)
    colordict = colordict.to_dict()['rgb']

    classes = dict()
    for n, (key, val) in enumerate(colordict.items()):
        classes[key] = (n, val)
    classes['NODATA'] = (n+1, 'rgb(0,0,0)')
    
    return classes


def gdf_to_rst(gdf, trs, w, h, path_to_desc):
    '''
    Convert a view of a gdf to a color-coded numpy array.
    '''
    unitcolor = generate_unitcolor_lookup(path_to_desc)
    rz = rasterize([(x.geometry, unitcolor.R[gdf.mapunit[i]]) for i, x in gdf.iterrows()],
                   out_shape=(w, h), transform=trs)
    gz = rasterize([(x.geometry, unitcolor.G[gdf.mapunit[i]]) for i, x in gdf.iterrows()],
                   out_shape=(w, h), transform=trs)
    bz = rasterize([(x.geometry, unitcolor.B[gdf.mapunit[i]]) for i, x in gdf.iterrows()],
                   out_shape=(w, h), transform=trs)
    
    return np.dstack((rz, gz, bz))


def clean_gdf_geometry(gdf):
    '''
    Expands MultiPolygon geometries into Polygon Geometries.
    gdf: A GeoPandas GeoDataFrame
    '''
    outdf = gpd.GeoDataFrame(columns=gdf.columns)
    for _, row in gdf.iterrows():
        if type(row.geometry) == Polygon:
            outdf = outdf.append(row, ignore_index=True)
        if type(row.geometry) == MultiPolygon:
            multdf = gpd.GeoDataFrame(columns=gdf.columns)
            recs = len(row.geometry)
            multdf = multdf.append([row]*recs, ignore_index=True)
            for geom in range(recs):
                multdf.loc[geom, 'geometry'] = row.geometry[geom]
            outdf = outdf.append(multdf, ignore_index=True)
    outdf.crs = gdf.crs
    
    return outdf


def normalize(array):
    '''
    Normalizes pixel values for display.
    '''
    array_min, array_max = array.min(), array.max()
    new_array = ((array - array_min)/(array_max - array_min))

    return new_array


def generate_label_array(path_to_rasterfile, path_to_azgeo='', path_to_desc=''):
    '''
    Collect the labels intersecting the bounds of the image, rasterize the labels, and return as a numpy aray.
    '''
    try:
        azgeo = gpd.read_file(path_to_azgeo)
    except:
        azgeo = gpd.read_file('https://raw.githubusercontent.com/azgs/geologic-map-of-arizona/gh-pages/data/MapUnitPolys.geojson')

    azgeo = clean_gdf_geometry(azgeo)

    with rasterio.open(path_to_rasterfile, 'r') as src:
        meta = src.meta.copy()
        trs = meta['transform']
        w, h = meta['width'], meta['height']
        
    raster_crs = meta['crs'].data
    azgeo = azgeo.to_crs(raster_crs)
    bbox = geometry.box(*src.bounds)
    gdf_temp = part_the_geojson(bbox, azgeo.copy())
    gdf = gdf_temp.loc[:, ['geometry', 'mapunit']]
    label_array = gdf_to_rst(gdf, trs, w, h, path_to_desc)
    
    return label_array


def format_label_fn(path_to_rasterfile):
    '''
    Given a filepath, return the 'labels' filename to write.
    '''
    if '/' in path_to_rasterfile:
        fn = path_to_rasterfile.split('/')[-1]
        path = path_to_rasterfile.replace(fn, '')
    else:
        fn = path_to_rasterfile
        path = ''
        
    tile = fn.split('_')[0]
    label_fn = tile + '_labels.tif'
    
    return path + label_fn


def write_label_image(label_array, path_to_rasterfile, fn_write):
    '''
    Write out the numpy array with the raster's geoinformation to a file.
    '''
    with rasterio.open(path_to_rasterfile, 'r') as src:
        meta = src.meta.copy()
        meta.update(dtype=str(meta['dtype']))
        w, h = meta['width'], meta['height']
        crs, trs = meta['crs'], meta['transform']
        
    r, g, b = np.dsplit(label_array, 3)
    r = r.reshape(w, h)
    g = g.reshape(w, h)
    b = b.reshape(w, h)
    
    with rasterio.open(fn_write, 'w', **DefaultGTiffProfile(count=3, width=w, height=h), crs=crs, transform=trs) as dst:
        for k, arr in [(1, r), (2, g), (3, b)]:
            dst.write(arr, indexes=k)

    return


def mask_raster(imgpth, lblpth):
    ''' 
    Writes out a tiff file ('_raster.tif') masked by 0
    for NODATA regions (e.g., outside of Arizona).
    '''
    with rasterio.open(lblpth, 'r') as lbl:
        msk = lbl.read_masks()
        nm = (msk/255).astype(rasterio.uint16)

    with rasterio.open(imgpth, 'r+') as src:
        meta = src.meta.copy()
        b1, b2, b3 = (src.read(band) for band in (1,2,3))
        b1 *= nm[0, :, :]
        b2 *= nm[1, :, :]
        b3 *= nm[2, :, :]

    name = imgpth.split('/')[-1] 
    path = imgpth.replace(name, '')
    outname = path + name.split('_')[0] + '_raster.tif'

    with rasterio.open(outname, 'w', **meta) as dst:
        for k, arr in [(1, b1), (2, b2), (3, b3)]:
            dst.write(arr, indexes=k)
            
    return

def get_tile_ids(bucket='tjds', prefix='geostacks/labels'):
    ''' 
    Queries AWS S3 bucket for the tile ids contained in a folder.
    '''
    s3 = boto3.client('s3')
    lab = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)['Contents']
    tile_ids = [i['Key'].split('/')[-1][:3] for i in lab if '.tif' in i['Key']]
    
    return tile_ids


def tile_train_test_split(tile_ids=list, test=[], n=3):
    ''' 
    Given a list of tile_ids ([ABC, SQS, SWE]) randomly choose n tiles to test.
    If test tiles are pre-defined, subtract from all to yield train.
    '''
    tiles = np.array(tile_ids)
    if test:
        train = list(set(tiles) - set(test))
    else:
        test = list(np.random.choice(tiles, a=n, replace=False))
        train = list(set(tiles) - set(test))
        
    return train, test

