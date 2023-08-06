import os

__all__ = ['dataset']

thispath = os.path.dirname(os.path.realpath(__file__))

#==============================================================================

def dataset(path='.'):
    """Get file path in the JunPy dataset."""
    dataset_dir = os.path.dirname(thispath + '/../../dataset/')
    return os.path.realpath(dataset_dir + '/' + path + '/')

#==============================================================================
