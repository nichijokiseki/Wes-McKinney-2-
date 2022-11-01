import pandas as pd
import numpy as np
# pandas对象都有一个用于将数据以pickle格式保存到磁盘上的方法to_pickle
frame = pd.read_csv("examples:ex1.csv")
frame.to_pickle("examples:frame_pickle")
# 可以通过pd.read_pickle直接读取被pickle化的数据
print(pd.read_pickle("examples:frame_pickle"))
# ⚠️pickle仅建议用于短期存储格式，原因是很难保证改格式永远是稳定的

# HDF5是一种存储大规模科学数组数据的非常好的文件格式
# 对于那些非常大的无法直接放入内存的数据集，HDF5是不错的选择，因为可以高效地分块读写
# pandas为访问HDF5文件提供了更为高级的接口，可以简化存储Series和DataFrame对象
