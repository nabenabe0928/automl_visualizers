# Motivation

# Requirements

# Implementation

```
$ python -m plot_funcs.<target file>
```

# ToDo
- visualize the final best pipeline
- analysing the sampling behavior (for 1D or 2D function)
=> multi dimensional scaler (MDS, t-sne) can help you visualize multi dimension
=> extension is to make the animation that adds configuraiton iteratively
- parallel coordinate plot (color stands for the ranking)
- violin-plot for each dimension

# Examples

# Times New Roman issues

When Times New Roman becomes bold, add the followings to `plot_funcs/__init__.py` which you would like to run:
```
import matplotlib

del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()
```

When Times New Roman is not available, run the followings from the command line:
```
$ sudo apt install msttcorefonts -qq
$ rm ~/.cache/matplotlib -rf
```
