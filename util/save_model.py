import appdirs
import os.path
import pystan
import pickle
import h5py
import numpy as np

def write_samples(samples,file,*params,**kwparams):
    with h5py.File(file,'w',*params,**kwparams) as store:
        for key in samples.keys():
            store[key] = samples[key]


def read_samples(file,*params,**kwparams):
    samples = {}
    with h5py.File(file,'r',*params,**kwparams) as store:
        for key in store.keys():
            x = np.zeros(store[key].shape,dtype=store[key].dtype)
            store[key].read_direct(x)
            samples[key] = x

    return samples

def load_model(prefix,nocache=False):
    if nocache:
        clear_cache(prefix,use_package_cache)
    else:
        model_file = prefix+".stan"
        object_file = prefix+".o"

    if not os.path.isfile(object_file):
        print ("WARNING: Saving cached model to "+object_file+" you will "+
               "need to delete this file if you want changes to "+model_file+
               " to take effect.")

        model = pystan.StanModel(model_file)
        with open(object_file,'wb') as f: pickle.dump(model,f)
    else:
        with open(object_file,'rb') as f: model = pickle.load(f)

    return model
