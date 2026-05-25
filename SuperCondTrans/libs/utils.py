# Utils
from types import SimpleNamespace
import shutil
import h5py
import os

#-----------------------------------------------------------

# Clean
def clean(path):
    '''
    Delete all contents of a folder and recreate it empty.

    Input:
    - path (str): Folder Path

    Output:
    - None

    Used by:
    - General Proposal
    '''

    shutil.rmtree(path, ignore_errors=True) # Delete Folder
    os.makedirs(path, exist_ok=True)        # Create Folder

    return None

#-----------------------------------------------------------

# Compress
def compress(path):
    '''
    Compresses a folder into a ZIP.

    Input:
    - path (str): Folder Path

    Output:
    - None
    - Folder ZIP 

    Used by:
    - General Proposal
    '''   

    shutil.make_archive(path, 'zip', path)  # Folder to ZIP
    shutil.rmtree(path, ignore_errors=True) # Delete Folder

    return None

#-----------------------------------------------------------

# To HDF5
def to_hdf5(path, **dataset):
    '''
    Save datasets to HDF5 file.

    Input:
    -     path (str): HDF5 File Path
    - dataset (?, ?): Dataset

    Output:
    - None
    - HDF5 File

    Used by:
    - General Proposal
    '''

    # Save
    with h5py.File(path, 'w') as file:
        for (key, value) in dataset.items():
            file.create_dataset(key, data=value)

    return None

#-----------------------------------------------------------

# From HDF5
def from_hdf5(path):
    '''
    Load datasets to HDF5 file.

    Input:
    -                path (str): HDF5 File Path

    Output:
    - dataset (SimpleNamespace): Dataset

    Used by:
    - General Proposal
    '''

    # Read
    with h5py.File(path, 'r') as file:
        data = {key: file[key][:] for key in file.keys()}
    dataset = SimpleNamespace(**data)
    
    return dataset