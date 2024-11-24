# import pandas as pd
# import numpy as np
#
# # 假设你的数据已经加载到 DataFrame 中
# # 读取数据
# df = pd.read_csv(r'I:\intan_new\Intan_control_control_10_240811_160453_control_10_240811_172453.rhd_sorting_auto_KS25.csv')
#
# # 删除时间列，保留神经元活动数据
# activity_data = df.drop(columns=['Time (s)'])
#
# # 初始化分支比率列表
# branching_ratios = []
#
# # 计算分支比率
# for t in range(len(activity_data) - 1):
#     parent_activity = activity_data.iloc[t].values  # 当前时间点的神经元活动
#     child_activity = activity_data.iloc[t + 1].values  # 下一时间点的神经元活动
#
#     # 父代激活神经元数量
#     num_parent_active = np.sum(parent_activity)
#
#     # 子代激活神经元数量
#     num_child_active = np.sum(child_activity)
#
#     # 计算分支比率（避免除以零的情况）
#     if num_parent_active > 0:
#         br = num_child_active / num_parent_active
#         branching_ratios.append(br)
#
# # 计算平均分支比率
# average_branching_ratio = np.mean(branching_ratios)
#
# print(f"Average Branching Ratio: {average_branching_ratio:.2f}")
#
# # 判断系统状态
# if average_branching_ratio > 1:
#     print("系统处于超临界态（Supercritical State）")
# elif average_branching_ratio < 1:
#     print("系统处于亚临界态（Subcritical State）")
# else:
#     print("系统处于临界态（Critical State）")

import pandas as pd
import numpy as np
import os
from tqdm import tqdm

# 设置数据文件夹路径
folder_path = r'I:\intan_new\spike_csv'

# 文件夹名列表
folders = ['control', 'lps7d', 'min7d']

# 用于存储文件名和分支比率的列表
file_branching_ratios = []

# 计算需要处理的文件总数
total_files = sum([len(os.listdir(os.path.join(folder_path, folder))) for folder in folders])

# 初始化进度条
with tqdm(total=total_files, desc="Processing Files", unit="file") as pbar:
    # 遍历所有文件夹
    for folder in folders:
        folder_dir = os.path.join(folder_path, folder)

        # 遍历文件夹中的所有csv文件
        for filename in os.listdir(folder_dir):
            if filename.endswith('.csv'):
                # 构造文件路径
                file_path = os.path.join(folder_dir, filename)

                # 读取数据
                df = pd.read_csv(file_path)

                # 删除时间列，保留神经元活动数据
                activity_data = df.drop(columns=['Time (s)'])

                # 初始化分支比率列表
                branching_ratios = []

                # 计算分支比率
                for t in range(len(activity_data) - 1):
                    parent_activity = activity_data.iloc[t].values  # 当前时间点的神经元活动
                    child_activity = activity_data.iloc[t + 1].values  # 下一时间点的神经元活动

                    # 父代激活神经元数量
                    num_parent_active = np.sum(parent_activity)

                    # 子代激活神经元数量
                    num_child_active = np.sum(child_activity)

                    # 计算分支比率（避免除以零的情况）
                    if num_parent_active > 0:
                        br = num_child_active / num_parent_active
                        branching_ratios.append(br)

                # 计算平均分支比率
                if branching_ratios:
                    average_branching_ratio = np.mean(branching_ratios)
                else:
                    average_branching_ratio = np.nan  # 如果没有有效的分支比率，设置为NaN

                # 将文件名和分支比率添加到列表中
                file_branching_ratios.append([filename, average_branching_ratio])

                # 更新进度条
                pbar.update(1)

# 创建数据框
result_df = pd.DataFrame(file_branching_ratios, columns=['Filename', 'Branching Ratio'])

# 导出数据框到CSV文件
result_df.to_csv(r'I:\intan_new\branching_ratios_output.csv', index=False)

print("数据已成功导出到 'branching_ratios_output.csv'")
