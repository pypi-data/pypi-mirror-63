import os

__all__ = ['dataset']

thispath = os.path.dirname(os.path.realpath(__file__))

#==============================================================================

def dataset(path='.'):
    """Get file path in the JunPy dataset."""
    return f'{thispath}/{path}'

#==============================================================================
