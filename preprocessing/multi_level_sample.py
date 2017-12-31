import sys
import os
import os.path as op
sys.path.append(os.path.abspath("."))

import util.slopes as slopes

slopes.run_slopes_model('standard_model',iters=2000,warmup=1000,chains=4,
                        cache_file='standard_model')
print "Please find the file with prefix 'standard_model' in the current directory."
print "Move that file to preprocessing/data/ and then manually update"
print "preprocessing/files.txt"
