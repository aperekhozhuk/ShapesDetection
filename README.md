# Detection simple shapes on binary image

Program detects next shapes on binary image:
1) Periods
2) Chains
3) Triangles
4) Rectangles (squares in particular)
5) Ellipses (circles in particular)
6) Just convex polygons

### **Input:**
binary image (stored in 'blob.jpg' by default), filters (optionally) for minimum length (for chains and periods only) and minimum area (for other shapes), alternative path to image file
### **Output:**
image with highlighted shapes (one color for each shape type), if filters provided - unfit shapes ignores

### **Programm running examples:**
1) Default file path, no filters
```
python3 Shapes.py
```
2) Alternative file path
```
python3 Shapes.py path/to/my_file.jpg
```
3) Filters for minimum length and area
```
python3 Shapes.py 400 10000
```
4) Filters and alternative file path
```
python3 Shapes.py 400 10000 path/to/my_file.jpg
```

### **Installing dependencies:** ###
##### 1) Create virtualenv (if you don't want install libs globally)
```
python3 -m venv env
```
##### 2) Activate virtualenv
###### Windows
```
env\Scripts\activate.bat
```
###### Linux
```
source env/bin/activate
```
##### 3) Install requirements
```
pip install -r requirements.txt
```
