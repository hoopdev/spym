import os
from . import rhksm4, omicronscala, nanonissxm

def load(filename, scaling=True, datatype_separate = False):
    ''' Import data from common SPM file formats.

    Currently supported file formats are:
        * NeXus (.nx, .nxs). Package nxarray is needed.
        * RHK (.sm4).
        * Omicron Scala (.par).

    Args:
        filename: path to the SPM file.
        scaling: if True convert data to physical units (default), if False keep raw data.
        datatype_separate: if True pages of images and lines are handled separately, if False handled altogether.

    Returns:
        if datatype_separate is True: List of xarray Datasets with data and metadata. The length of the list is two.
        if datatype_separate is False: xarray Dataset with data and metadata.

    '''

    if filename.endswith(".nx") or filename.endswith(".NX") or filename.endswith(".nxs") or filename.endswith(".NXS"):
        try:
            import nxarray
        except ImportError:
            print("Error: nxarray package is needed to open .nx/.nxs files.")
            return None
        try:
            ds = nxarray.load(filename)
        except:
            print("Error: the file does not appear to be valid.")
            return None

    if filename.endswith(".par") or filename.endswith(".PAR"):
        try:
            ds = omicronscala.to_dataset(filename, scaling=scaling)
        except:
            print("Error: the file does not appear to be valid.")
            return None

    if filename.endswith(".sm4") or filename.endswith(".SM4"):
        try:
            ds = rhksm4.to_dataset(filename, scaling=scaling,datatype_separate=datatype_separate)
        except:
            print("Error: the file does not appear to be valid.")
            return None


    #TODO
    '''
    if filename.endswith(".sxm") or filename.endswith(".SXM"):
        try:
            ds = nanonissxm.to_dataset(filename, scaling=scaling)
        except:
            print("Error: the file does not appear to be valid.")
            return None
    '''
    if datatype_separate:
        for dr in ds[0]:
            ds[0][dr].attrs["filename"] = os.path.basename(filename)
        for dr in ds[1]:
            ds[1][dr].attrs["filename"] = os.path.basename(filename)
    else:
        for dr in ds:
            ds[dr].attrs["filename"] = os.path.basename(filename)

    return ds

def convert(filename, folder=None):
    ''' Convert data from supported SPM file formats to NeXus/HDF5.

    Args:
        filename: path to the SPM file.
        folder: (optional) path for converted files. If not provided, converted files are placed in the same folder of the originals.

    Returns:
        Nothing.

    '''

    ds = load(filename, scaling=False)

    try:
        import nxarray
        filename = os.path.splitext(filename)[0]
        if folder:
            path = os.path.join(folder, os.path.basename(filename))
        else:
            path = filename
        ds.nxr.save(path)
    except ImportError:
        print("Error: nxarray package is needed to convert files.")
