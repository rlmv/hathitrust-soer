from __future__ import absolute_import

import os

try:
    from . import ptree
except ValueError:
    import ptree



class PairTreePathFinder(object):
    """Class to access HathiTrust pairtree collections. 

    Maps htids onto a pairtree collection. We assume the standard HathiTrust
    collection specification, e.g.
        /path_to_collection/namespace/'pairtree_root'/pairtree_path/id_directory

    Usage:
        >>> pf = PairTreePathFinder("Volumes/home/bo.marchman/non_google)
        >>> pf.get_path_to_htid("dul1.ark:/13960/t00z7x54f")
        /Volumes/home/bo.marchman/non_google/dul1/pairtree_root/ar/k+/=1/39/60/=t/00/z7/x5/4f/ark+=13960=t00z7x54f
    """

    def __init__(self, collection_path):
        """ 
            Args:
            - collection_path: path to the root of the HathiTrust collection.
        """
        collection_path = os.path.abspath(collection_path)
        if not os.path.isdir(collection_path):
            raise ValueError("{} is not a valid directory.".format(
                    collection_path))
        self.cpath = collection_path


    def get_path_to_htid(self, htid):
        """ Returns the path to the pairtree directory for this htid.

            Args should include the id namespace, eg:
                dul1.ark:/13960/t00z7x54f
                uc2.ark:/13960/t9p26rn3h
                etc.

            Returns a tuple - (path, postfix)
        """

        ns, post = htid.split('.')
        posttree = ptree.id2ptree(post)
        posttree = posttree.strip('/') # / at front of string break path join
        post = self.encode(post) # replace :, /, etc.

        l = [self.cpath, ns, 'pairtree_root', posttree, post]
        fullpath = os.path.join(*l)

        if not os.path.exists(fullpath):
            raise ValueError("Is id {} in the collection? Path {} not found."
                    .format(htid, fullpath))
        return fullpath, post


    def encode(self, htid):
        """ Transform a HathiTrust id into POSIX compatible equivalent. """
        return ptree._encode(htid)


if __name__ == "__main__":

    pf = PairTreePathFinder("/Volumes/home/bo.marchman/non_google")
    print(pf.get_path_to_htid('dul1.ark:/13960/t00z7x54f'))


