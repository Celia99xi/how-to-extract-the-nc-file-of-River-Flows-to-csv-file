# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 15:50 2023

@author: Xi Wang
"""

import numpy as np
import netCDF4 as nc
import csv
import os
from datetime import datetime, timedelta

# 输入文件路径和输出文件夹路径
input_file = 'G:/DaBaiCai/GRADES_Q_v01_pfaf_01_19790101_20131231.nc'
output_folder = 'G:/DaBaiCai/Output_date/'

# 打开NetCDF文件
nf = nc.Dataset(input_file)

# 获取 "Q" 变量的维度
num_times = nf.dimensions['time'].size
num_COMID = nf.dimensions['COMID'].size

# 定义块大小
block_size = 1000  # 每个块包含1000个COMID

# 生成日期序列从 "1979-01-01" 到 "2013-12-31"
start_date = datetime(1979, 1, 1)
date_list = [(start_date + timedelta(days=i)).strftime('%Y_%m_%d') for i in range(num_times)] #格式化为"YYYY_MM_DD" 形式


# 检查输出文件夹是否存在，如果不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 逐块读取和处理数据
for i in range(0, num_COMID, block_size):
    start_COMID = i
    end_COMID = min(i + block_size, num_COMID)

    # 读取部分 "Q" 数据
    Q_data_block = nf['Q'][:, start_COMID:end_COMID]

    # 将MaskedArray转换为普通的numpy.ndarray
    Q_data_block = np.ma.filled(Q_data_block, fill_value = -999)   # 将缺失值填充为特殊值如-999

    # 创建输出文件名
    output_file = output_folder + f'Q_data_block_{start_COMID}_{end_COMID}.csv'

    # 保存块数据为CSV文件
    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # 写入CSV文件的标题行，包括日期列
        header_row = ['Date'] + [f'COMID_{i}' for i in range(start_COMID, end_COMID)]
        writer.writerow(header_row)

        # 写入数据行
        for time_index in range(num_times):
            row = [date_list[time_index]] + list(Q_data_block[time_index])
            writer.writerow(row)

# 关闭NetCDF文件
nf.close()
