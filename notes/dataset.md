For the past few weeks I've been working with the HathiTrust's 300,000 document non-Google digitized public domain collection. It's easy enough to get your hands on the dataset; it is, after all, public domain and as such has no access restrictions--all it takes is a quick email to HathiTrust. They prefer to distribute the collection via [rsync][rsnyc], and once your IP address is authorized on their server you're good to go. (Rsync is interesting in and of itself--it provides efficient file transfers and updates, and allows interrupted sessions to be completed without resending all data. The algorithm is actually quite clever and fairly simple; if you're interested, the paper is [here][rsync algo])

[rsync]: http://rsync.samba.org/
[rsync algo]: http://cs.anu.edu.au/techreports/1996/TR-CS-96-05.pdf

The non-Google public domain collection is about 200Gb, so not a trivial amount to save locally. I initially stored the dataset on the BeSTGRID Data Fabric, NeSI's data repository, which is easy to set up and use (the [documentation][data fabric] on the eResearch Wiki is excellent), and can be mounted on a local machine with the WebDAV protocol, allowing command line access.  However, WebDAV is a network protocol and I quickly ran into latency problems--read requests take a second or so per file which becomes significant when computing over 300,000 documents. So, as of now, I've moved the dataset to an external hard-drive which is proving significantly faster.

[data fabric]: https://wiki.auckland.ac.nz/display/CERES/Data+Fabric+Access

Pairtree structure
------------------
HathiTrust structures its datasets in a pairtree file hierarchy, which specifies a mapping of indentifiers onto native directory trees. Typical filesystems do not handle large numbers of files in a single directory well; depending on the platform, searching can become very ineffiecient. The pairtree heirarchy mitigates this by balancing the depth and width of the directory structure as follows: Suppose we have a file identifier, e.g. `t1zc80f9r`. We split the id into consecutive pairs, and assign each pair to a level in the directory hierarchy

    t1zc80f9 --> t1/zc/80/f9/

Now, suppose we have another similar id:

    t1zc81g7 --> t1/zc/81/g7/

Together, these translate to a literal file structure

    t1/
    |
    \---zc/
        |
        \---80/
        |   |
        |   \---f9/
        |
        \---81/
            |
            \---g7/

Given an identifier we can quickly find a file in the pairtree structure by computing the directory division, and given a file in the pairtree structure, we can quickly compute the file's id by traversing the directory tree. This leads to an efficient, platform independent, software independent (no database required!) way to store large collections. Of course there's more to the specification than what I've described; you can read all the details [here][pairtree spec]. 

There are a few Python packages for dealing with pairtree filestructures: The [Pairtree][Pairtree] module is extensive and handles mapping identifiers, creating, and reading to and from pairtree hierarchies. This is more functionalality than I need though, so I've opted to use [ptree][ptree], which just handles identifier mappings and leaves all other operations up to the programmer. 

[pairtree spec]: http://tools.ietf.org/pdf/draft-kunze-pairtree-01.pdf
[Pairtree]: http://pypi.python.org/pypi/Pairtree
[ptree]: https://github.com/edsu/ptree

So what do we get?
=====================
Besides a file listing all document identifiers in the collection, HathiTrust datasets include the following:

OCR Text
--------
This is the raw OCR (Optical Character Recognition) text. Each document is a zip archive of text files, one file per page, of OCR text. 

METS
-----
METS stands for Metadata Encoding and Transmission Standard, and is an XML schema for storing metadata specific to digital objects. The METS files include bibliographic entries (MARC records), information about the digitization process, and a description of the document structure, in this case the OCR text. More information about the HathiTrust's specific schema is [here][METS].

[METS]: http://www.hathitrust.org/digital_object_specifications

MARC XML
--------
A copy of the MARC bibliographic records are provided for each document, both in the METS files and in a single concatenated 800Mb file. MARC is standard bibliographic data, detailing author, title, publisher, topic and other card-catalog information.




