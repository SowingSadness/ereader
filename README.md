ereader
=======

Effective news site reader.


Install
=======
    
    
    pip install virtualenv
    virtualenv ereader
    . env/bin/activate

    pip install -r requirements.txt

    python setup.py install

Configure
=========

    See at ereader/ereader.ini
    

Usage
=====

    
    ereader http://www.bbc.com/news/world-middle-east-34375875

    Custom config:

        ereader -c ~/.ereader.ini http://www.bbc.com/news/world-middle-east-34375875

    Short view:

        ereader -v 3 --short http://www.bbc.com/news/world-middle-east-34375875

Tests
=====

    make test-urls

