# Utils
import shutil
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