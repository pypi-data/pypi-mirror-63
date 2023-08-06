### Installation
The module, python-interpol requires pandas module to function
This module is used to predict the target feature using langranges' interpolation extended to multivariate case by first remove duplicates and ambiguities in the dataset. The first column of the csv file should be that of the target class or feature while the others be independent features affecting target feature.

Usages: python-dupamb <InputDataFile> <InputXTuple> <Weights>
	
```sh
$ pip install python-interpol
$ python-interpol myData.csv 2,3,4,5 0.25,0.25,0.25,0.25
```
### License
MIT
### Author
Sahil Ahuja
