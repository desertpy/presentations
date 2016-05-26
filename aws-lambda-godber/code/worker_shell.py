import os
import sys
import rasterio

def main():
    filename = '/tmp/foo.txt'
    with open(filename, 'w') as f:
        f.write('this is a test')

    return filename

if __name__ == "__main__":
    print main()
