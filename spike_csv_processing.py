import os  # 导入操作系统相关的模块，用于文件和目录的操作
import spikeinterface.full as si  # 导入 spikeinterface 库，处理神经数据
import numpy as np  # 导入 numpy，用于数值计算
import pandas as pd  # 导入 pandas，用于数据处理和数据框操作
import sys  # 导入 sys，用于获取命令行参数
from tqdm import tqdm  # 导入 tqdm，用于显示循环的进度条


# 递归查找所有以 .rhd_sorting_auto_KS25 结尾的文件夹
def find_sorting_folders(base_path):
    sorting_folders = []  # 用于存储找到的符合条件的文件夹路径
    for root, dirs, files in os.walk(base_path):  # 遍历根目录下的所有子目录
        for dir_name in dirs:  # 遍历所有的子目录名称
            if dir_name.endswith('rhd_sorting_auto_KS25'):  # 判断目录是否以指定后缀结尾
                sorting_folders.append(os.path.join(root, dir_name))  # 如果符合条件，添加到列表中
    return sorting_folders  # 返回找到的所有符合条件的文件夹路径


# 保存结果到 CSV 文件
def save_results_to_csv(results, output_file):
    df = pd.DataFrame(results)  # 将结果转换为 pandas 数据框
    df.to_csv(output_file, index=False)  # 保存数据框为 CSV 文件


# 主函数，处理找到的所有文件夹
def process_sorting_data(base_path, output_folder, bin_size_ms=40):
    sorting_folders = find_sorting_folders(base_path)  # 查找所有符合条件的文件夹

    for folder in tqdm(sorting_folders, desc="Processing folders", unit="folder"):  # 使用 tqdm 显示处理进度
        try:
            # 从文件夹中加载排序数据
            sorting_auto = si.load_extractor(folder)

            # 参数初始化
            segment_index = None
            unit_ids = None
            time_range = None

            # 确定分段索引
            if segment_index is None:
                if sorting_auto.get_num_segments() != 1:  # 如果分段数量不为 1，则必须手动提供 segment_index
                    raise ValueError("You must provide segment_index=...")
                segment_index = 0  # 如果只有一个分段，则默认设置为 0

            # 确定时间范围
            if time_range is None:
                frame_range = [0, sorting_auto.to_spike_vector()[-1]["sample_index"]]  # 获取帧范围
                time_range = [f / sorting_auto.sampling_frequency for f in frame_range]  # 将帧转换为时间范围（秒）
            else:
                assert len(
                    time_range) == 2, "'time_range' should be a list with start and end time in seconds"  # 确保时间范围是开始和结束时间的列表
                frame_range = [int(t * sorting_auto.sampling_frequency) for t in time_range]  # 将时间转换为帧范围

            sampling_frequency = sorting_auto.get_sampling_frequency()  # 获取采样频率
            bin_size = bin_size_ms / 1000  # 将时间窗大小从毫秒转换为秒

            # 创建时间窗（bin）
            num_bins = int(np.ceil((time_range[1] - time_range[0]) / bin_size))  # 计算时间窗的数量
            time_bins = np.linspace(time_range[0], time_range[1], num_bins + 1)  # 生成等间距的时间窗边界

            # 初始化二进制脉冲矩阵
            all_unit_ids = sorting_auto.get_unit_ids() if unit_ids is None else unit_ids  # 获取所有单元 ID
            binary_spike_matrix = np.zeros((len(all_unit_ids), num_bins))  # 创建一个用于存储脉冲数据的矩阵

            # 填充二进制脉冲矩阵
            for unit_index, unit_id in enumerate(all_unit_ids):  # 遍历每个单元
                spiketrain = sorting_auto.get_unit_spike_train(
                    unit_id,
                    start_frame=frame_range[0],
                    end_frame=frame_range[1],
                    segment_index=segment_index,
                )  # 获取该单元的脉冲序列
                spiketimes = spiketrain / float(sampling_frequency)  # 将帧索引转换为时间（秒）
                spike_bins = np.digitize(spiketimes, time_bins) - 1  # 找到每个脉冲所属的时间窗索引
                binary_spike_matrix[unit_index, spike_bins] = 1  # 将相应位置设置为 1，表示在该时间窗有脉冲

            # 创建一个 DataFrame 保存脉冲矩阵
            binary_spike_df = pd.DataFrame(binary_spike_matrix.T, columns=all_unit_ids)  # 转置矩阵并创建 DataFrame
            binary_spike_df['Time (s)'] = time_bins[:-1]  # 添加时间列

            # 生成输出 CSV 文件的名称，基于文件夹名称
            output_filename = os.path.basename(folder) + '.csv'  # 以文件夹名命名 CSV 文件
            output_path = os.path.join(output_folder, output_filename)  # 构造完整的输出路径

            # 将脉冲数据保存到 CSV 文件中
            binary_spike_df.to_csv(output_path, index=False)  # 保存 DataFrame 为 CSV 文件
            print(f"Saved: {output_path}")  # 打印保存成功的信息

        except Exception as e:
            print(f"Error processing {folder}: {e}")  # 打印错误信息


# 从命令行获取路径
if __name__ == "__main__":
    if len(sys.argv) != 3:  # 检查命令行参数的数量
        print("用法: python 批量提取RHD文件夹数据.py <根文件夹路径> <输出文件夹路径>")  # 打印用法提示
    else:
        base_path = sys.argv[1]  # 获取根文件夹路径
        output_folder = sys.argv[2]  # 获取输出文件夹路径
        # 如果输出文件夹不存在，则创建它
        os.makedirs(output_folder, exist_ok=True)  # 创建输出文件夹
        # 处理所有符合条件的文件夹
        process_sorting_data(base_path, output_folder)  # 调用主函数处理数据


# python spike_csv_processing.py I:\intan_new\min3d I:\intan_new\ I:\intan_new\spike_csv\min3d