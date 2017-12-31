import sys
import os
import os.path as op
sys.path.append(os.path.abspath("."))

import util.slopes as slopes

slopes.run_slopes_model('musician_model',iters=2000,warmup=1000,chains=4,
                        cache_file='musician_model')
print "Please find the file with prefix 'musician_model' in the current directory."
print "Move that file to preprocessing/data/ and then manually update"
print "preprocessing/files.txt"
