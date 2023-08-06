


# **OUTLIER REMOVAL USING IQR METHOD**


### Author : **Mehak Garg**


## **What are outliers?**

An outlier is an observation that lies an abnormal distance from other values in a random sample from a population.
In a sense, this definition leaves it up to the analyst (or a consensus process) to decide what will be considered abnormal. 
Before abnormal observations can be singled out, it is necessary to characterize normal observations.


## **What is IQR method?**

A robust method for labelling outliers is the IQR (interquartile range) method of outlier detection developed by John Tukey, the pioneer of exploratory data analysis. 
This was in the days of calculation and plotting by hand, so the datasets involved were typically small, and the emphasis was on understanding the story the data told. 
A box-and-whisker plot (also a Tukey contribution), shows this method in action.

A box-and-whisker plot uses quartiles (points that divide the data into four groups of equal size) to plot the shape of the data. 
The box represents the 1st and 3rd quartiles, which are equal to the 25th and 75th percentiles. The line inside the box represents the 2nd quartile, 
which is the median.

The interquartile range, which gives this method of outlier detection its name, is the range between the first and the third quartiles (the edges of the box). 
Tukey considered any data point that fell outside of either 1.5 times the IQR below the first – or 1.5 times the IQR above the third – quartile to be outside or far out. 
In a classic box-and-whisker plot, the 'whiskers' extend up to the last data point that is not outside.



## **How to use this package:**

It take in the dataset csv file and outputs out a csv file in the rows having outlier values are removed. This package handles univariate datasets as well as multivariate. 
Each feature having outlier rows are removed.

### **Installation**

The package can be installed using the following command in anaconda/command prompt.

~~~
pip install outlier-removal_3054
~~~

### **Usage**

The package can be used for outlier removal by providing dataset.

~~~
remove-outlier <dataset>
~~~
