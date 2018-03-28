# NOTE: you should not normally have to run this
# but if you run into problems activating the environment
# these are the commands I used to create it.
#
# BEWARE: you'll quite possibly end up with newer versions of
# the software, so this may break the code in small ways.
# (Usually this will invovle reading error messages and fixing
# the code appropriately)


conda create --channel conda-forge --override-channels --name apmusic_2018_03_02 python=2.7
source activate apmusic_2018_03_02
conda install -c conda-forge r-base r-tidyr r-dplyr r-ggplot2 pystan r-cowplot r-stringr pymc3 scipy numpy pandas ipython h5py 
