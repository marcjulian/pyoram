class FileMap:
    # fields in the filemap: file name, file size, list of dataIDs
    # dataID is a counter (dataID maybe random to always have the same size, so it can be stored within the ciphertext)
    def __init__(self):
        print('file.map')


class PositionMap:
    # fields in the positionmap: dataId, leafID, iv, hash (maybe iv and hash must be stored in file map)
    # leafID is random
    def __init__(self):
        print('position.map')
