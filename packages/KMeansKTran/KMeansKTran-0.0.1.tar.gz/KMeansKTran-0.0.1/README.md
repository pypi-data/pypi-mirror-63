# KMeansKTran
K-Means Clustering package to find best K using Silhouette Analysis

To run the script, use **run_KMeans()** method.

Arguments for **run_KMeans(filenames, output)**

**filenames**: list

>List of strings to designate text filenames or file locations with filenames
>
>Example: ["C:\\Folder\\File1.txt"]
  
**output**: string

>String to designate location of output text file with filename
>
>Example: "C:\\Folder\\output.txt"

**Example**
```python
from KMeans_KTran import kmeans

kmeans.run_KMeans(["C:\\Folder\\File1.txt"], "C:\\Folder\\output.txt")
```