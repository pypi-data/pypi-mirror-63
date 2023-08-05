# Introduction

Point_viz is a light-weight, out-of-box point cloud visualizer working in browser, it is built on [Three.js](https://threejs.org)
and has python API. Bounding box (bbox) visualization is supported and here is an [example](). 
Point_viz does not need Internet connection to work (but the installation needs, of course), 
and it has been tested on Chrome and Safari with both python 2 and 3.

# Usage
To install point_viz, simply run: `pip install point_viz`, and that's all. Below is the example of its python API:
```
# Import package.
from point_viz import PointvizConverter

# Initialize and setup output directory.
Converter = PointvizConverter(home)
# Pass data and create html files.
Converter.compile(task_name, coors, default_rgb, intensity, bbox_params, bbox_color)
```

###  Variables Explanation

###### The `*` means optional. 
**home**: The directory where to put output html files, must be given. \
**task_name***: _string_, name of the output html file (can be overwritten if the name already exists; default value is "default").\
**coors***: _2-D float array_, the x, y and z coordinates of each point in the point cloud.\
**default_rgb***: _2-D float/int array_ of the same length as `coors`, the R, G and B colors of each point. 
If not provided, the RGB will be automatically calculated based on `intensity` (if given) or 
point coordinates (when `intensity` is also missing).\
**intensity***: _1-D float array_ of the same length as `coors`, the intensity of each point. It only takes effect when
`default_rgb` is not given.\
**bbox_params***: _2-D list_, the geometry parameters of each bbox. Attributes of each row should be arranged as follows:


| Attribute # | Description  |
|---|---|
| 0  | Length (_float_, dimension along x-axis)  |
| 1 | Height (_float_, dimension along y-axis) |
| 2  | Width (_float_, dimension along z-axis)  |
|3  | X coordinate of bbox centroid  (_float_)  |
| 4  | Y coordinate of bbox centroid  (_float_)  |
| 5  | Z coordinate of bbox centroid  (_float_)   |
| 6  | Horizontal rotation regarding the +x-axis in radians (_float_)   |
| 7*  | Color of the bbox (_string_, optional; [X11 color name](https://en.wikipedia.org/wiki/X11_color_names) is supported, default is "Magenta")   |
| 8*  | Label text of the bbox (_string_, optional)    |

**bbox_color***: _boolean_, default is `True`. If the color of bbox is missing while the label text is given, then 
`bbox_color` has to be explicitly set to `False`. 