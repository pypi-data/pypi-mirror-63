# Accelerometer Feature Extractor (AFE) #

This library is used to extract features from accelerometer data.  Features include e.g. frequency of motion, mean acceleration (vector magnitude), etc.  The features are meant to be useful to classify activity type, disease state, or whatever labels you have for your accelerometer data.

### How do I get set up? ###

You will need Python 3 with `numpy`, `scipy`, and `pandas`.

You will also need one of my other libraries, `actigraph`, which is also in PyPI.  However, that library is only used to compute one feature, and you could safely remove the dependency from `features.py` if you didn't want to use it.

To install from PyPI:

    pip3 install afe

Or from git:

    git clone https://bitbucket.org/atpage/afe.git
    cd afe
    pip3 install -e .

### How do I run it? ###

First, create a pandas DataFrame containing your accelerometer samples.  The index should be time (as either a timestamp, or number of seconds), and the columns should be named `x`, `y`, and `z`.  If you have gyroscope data as well, include those columns as `rx`, `ry`, and `rz`.  Any axis can be omitted if your hardware didn't include it.  Then:

    # my data is already stored in df
    
    from afe import AFE
    afe = AFE(df)
    features = afe.get_features(window_size=60, overlap=0)
    
    # features is a new DataFrame with a row for each 60-second window, and a column for each feature.

### How do I add more features? ###

I'm still cleaning this up.  But for now, the process is:

1. Add a function in `features.py` that accepts two DataFrames: `data` and `epochs`.  `epochs` is the results DataFrame; your function will edit it in place by adding column(s) to it for your feature(s).  Your function will probably also need to accept `window_size` or `overlap`, which describe the duration of each epoch, since the `epochs` DataFrame only tells you the start time of each window.  Your function may also accept sample rate `sr` as a parameter, but most of the time it should be computable from `data.index` anyway.  Here is an example of a custom feature extractor:

        def extract_max_accel(**kwargs):
            data = kwargs.get('data')
            epochs = kwargs.get('epochs')
            window_size = kwargs.get('window_size')
            # don't pop() from kwargs!  other functions will probably be getting it after you.
            groups = data.groupby( (data.index - data.index[0]) // window_size )
            epochs['vm_max'] = groups.max().vm.values

2. Once you've created this function, add it to the `function_feature_map` to tell which new features (columns in `epochs`) it will be adding:

        function_feature_map = {
            ... # stuff was already here
            
            extract_max_accel: ['vm_max'],
        
            ... # other stuff was already here
        }

That's it!  Your function should run automatically with `get_features()`.  You can try running `pytest` to confirm that it at least doesn't crash.

Note that your function may need to handle different types of `Index` of the incoming DataFrames.  The index may be either timestamps or floats.  Also, in the example above, we refer to `data.vm`, the vector magnitude acceleration.  This is automatically computed before features are extracted; it doesn't need to be part of your raw DataFrame.

### Who do I talk to? ###

* Alex Page, alex.page@rochester.edu
