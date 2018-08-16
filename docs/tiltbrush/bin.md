
## unpack_tilt.py

This program can be used to convert a tilt brush sketch into a 
directory format and vice-versa. By default files saved from 
Tilt Brush are saved in a archived format, but by unpacking them 
into a directory format we will still be able to load them in 
Tilt Brush. The advantage of the directory format is that we can 
see the thumbnail of the sketch and also other metadata stored in 
a .json file.

    C:\Users\sgoda\code\tilt-brush-toolkit\bin>python unpack_tilt.py
    usage: unpack_tilt.py [-h] [--compress] files [files ...]
    unpack_tilt.py: error: too few arguments
    
    C:\Users\sgoda\code\tilt-brush-toolkit\bin>python unpack_tilt.py "C:\Users\odw\Documents\Tilt Brush\Sketches\Untitled_4.tilt"
    Converted C:\Users\odw\Documents\Tilt Brush\Sketches\Untitled_4.tilt to directory format
    
    C:\Users\sgoda\code\tilt-brush-toolkit\bin>python unpack_tilt.py "C:\Users\odw\Documents\Tilt Brush\Sketches\Untitled_5.tilt"
    Converted C:\Users\odw\Documents\Tilt Brush\Sketches\Untitled_5.tilt to zip format