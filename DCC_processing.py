


import os
import criticality as cr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys  # 导入 sys 模块，用于获取命令行参数


# 查找所有以 .csv 结尾的文件
def find_csv_files(base_path):
    csv_files = []
    for root, dirs, files in os.walk(base_path):  # 遍历目录
        for file in files:  # 遍历所有文件
            if file.endswith('.csv'):  # 找到以 .csv 结尾的文件
                csv_files.append(os.path.join(root, file))  # 将文件的完整路径添加到列表中
    return csv_files  # 返回所有找到的 CSV 文件路径


# 处理 CSV 文件并获取 DCC 指标
def process_csv_files(base_path, output_folder):
    csv_files = find_csv_files(base_path)  # 获取所有 CSV 文件
    results = []  # 用于保存结果
    output_file = os.path.join(output_folder, 'DCC_results.xlsx')

    # 创建输出文件路径并确保它是 .xlsx
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 如果存在之前保存的结果，读取它们
    processed_files = set()  # 存储已处理过的文件名
    if os.path.exists(output_file):
        results_df = pd.read_excel(output_file, engine='openpyxl')
        results = results_df.to_dict('records')
        processed_files = set(results_df['File Name'].values)  # 读取已处理过的文件名

    # 仅处理未处理过的文件
    for csv_file in tqdm(csv_files, desc="Processing CSV files", unit="file"):
        file_name = os.path.basename(csv_file)
        if file_name in processed_files:
            print(f"Skipping already processed file: {file_name}")
            continue  # 跳过已处理过的文件

        try:
            # 读取 CSV 文件
            data = pd.read_csv(csv_file)
            print(f"Processing file: {csv_file}")

            # 准备数据
            time_bins = data['Time (s)']
            binary_spike_matrix = data.drop(columns=['Time (s)'])  # 去掉时间列
            data_transposed = binary_spike_matrix.transpose()  # 转置矩阵

            # 设定阈值
            perc = 0.25                  ###control: 0.5; 0.25  0.20  lps7d: 0.25; min7d: 0.25

            # 获取所有的 avalanche 并创建两个数组 S 和 T
            r = cr.get_avalanches(data_transposed, perc)
            burst = r['S']
            T = r['T']

            # 设置参数
            params = {
                'flag': 2,
                'bm': 30,                ###control: 40; 30                 lps7d:30                                  min7d: 30
                'tm': 10,                ###control: 15                     lps7d:15                                  min7d: 15; 10
                'exclude_burst': 20,     ###control: 20                     lps7d:20                                  min7d: 20
                'exclude_time': 20,      ###control: 20                     los7d:20                                  min7d: 20
                'pltname': file_name.replace('.csv', ''),  # 使用 CSV 文件名作为图形名称
                'saveloc': base_path,  # 将图表保存到输入文件夹中
                'plot': True  # 生成图表
            }

            # 运行 AV_analysis 获取 DCC 指标
            Result = cr.AV_analysis(burst, T, **params, nfactor_bm=2, nfactor_tm=1,          ###control: nfactor_bm: 2; nfactor_tm: 2                                                       lps7d: nfactor_bm: 2; nfactor_tm: 2                          min7d: nfactor_bm: 2; nfactor_tm: 2
                                    nfactor_bm_tail=0.85, nfactor_tm_tail=0.90,               ###control: nfactor_bm_tail: 0.80, 0.75; nfactor_tm_tail: 0.90                                 lps7d: nfactor_bm_tail: 0.75; nfactor_tm_tail: 0.90          min7d: nfactor_bm_tail: 0.85;0.80; 0.70 nfactor_tm_tail: 0.90
                                    none_fact=40, max_time=2400)                             ###control: 40; 2400                                                                           lps7d: 40; 2400                                              min7d: 40; 2400

            # 获取 DCC 值并保存到结果中
            dcc_value = Result['df']
            P_t = Result['P_t']
            P_burst = Result['P_burst']
            alpha = Result['alpha']
            beta = Result['beta']
            result = {
                'File Name': file_name,
                'DCC': dcc_value,
                'P_t': P_t,
                'P_burst': P_burst,
                'alpha': alpha,
                'beta': beta,
                'perc': 0.25,
                'bm': 30,
                'tm': 10,
                'exclude_burst': 20,
                'exclude_time': 20,
                'nfactor_bm': 2,
                'nfactor_tm': 1,
                'nfactor_bm_tail': 0.85,
                'nfactor_tm_tail': 0.90,
                'none_fact': 40
            }
            results.append(result)

            # 每处理完一个文件，立即保存结果
            results_df = pd.DataFrame(results)
            results_df.to_excel(output_file, index=False, engine='openpyxl')

        except Exception as e:
            print(f"Error processing {csv_file}: {e}")

    print(f"Results saved to: {output_file}")


# 从命令行获取路径
if __name__ == "__main__":
    if len(sys.argv) != 3:  # 检查命令行参数的数量
        print("用法: python 批量处理DCC指标.py <根文件夹路径> <输出文件夹路径>")  # 打印用法提示
    else:
        base_path = sys.argv[1]  # 获取根文件夹路径
        output_folder = sys.argv[2]  # 获取输出 Excel 文件夹路径
        # 处理所有符合条件的 CSV 文件并保存结果
        process_csv_files(base_path, output_folder)  # 调用主函数处理数据
