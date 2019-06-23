I ran the program using python 3.7.3 64-bit on windows
command to run program:
python partA.py #NumOfDataSet #NumOfAlgorithm

Number of data set can only be 0 or 1:
0 -> occupany_A
1 -< occupany_B

Number of algorithm can only be 0 or 1:
0 -> ID3 Algorithm
1 -> ID3 with five fold cross validation

Example:
python partA.py 0 0
runs question 1

python partA.py 0 1
runs question 2

python partA.py 1 1
runs question 3

Before running the python file, make sure to install a few libraries
anytree:
pip3 install anytree

graphziv:
pip3 install graphziv

matplotlib:
pip3 install matplotlib
