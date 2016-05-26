import os
import subprocess
import uuid

libdir = os.path.join(os.getcwd(), 'local', 'lib')

# Download the raster locally
download_path = '/tmp/srtm_21_09.tif'

# Call the worker, setting the environment variables
command = 'LD_LIBRARY_PATH={} python worker.py "{}"'.format(libdir, download_path)
output_path = subprocess.check_output(command, shell=True)

# Upload the output of the worker to S3
print output_path.strip()

