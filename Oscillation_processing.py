import os
import numpy as np
import pandas as pd
import sys
import spikeinterface.full as si
from probe_setup import create_square_probe
from spikeinterface.extractors import read_intan
import matplotlib.pyplot as plt
import matplotlib
from tqdm import tqdm  # 导入tqdm
from scipy.signal import stft


# 递归查找所有以.rhd_preprocessed结尾的文件夹
def find_preprocessed_folders(base_path):
    preprocessed_folders = []
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            if dir_name.endswith('.rhd_preprocessed'):
                preprocessed_folders.append(os.path.join(root, dir_name))
    return preprocessed_folders


# 保存结果到CSV
def save_results_to_csv(results, output_file):
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)


# 主函数
def process_folders(base_path, output_file):  # 接受两个参数
    preprocessed_folders = find_preprocessed_folders(base_path)
    all_results = []

    for folder in tqdm(preprocessed_folders, desc="Processing folders", unit="folder"):
        try:
            recording_saved = si.load_extractor(folder)
            fs = recording_saved.get_sampling_frequency()

            band_names = ['delta', 'theta', 'alpha', 'beta', 'low_gamma', 'high_gamma']   #####
            freq_ranges = [(1, 4), (4, 8), (8, 12), (12, 30), (30, 50), (50, 100)]

            for i in range(recording_saved.get_num_channels()):
                results = []
                for band, (freq_min, freq_max) in zip(band_names, freq_ranges):
                    recording_band = si.bandpass_filter(recording_saved, freq_min=freq_min, freq_max=freq_max)
                    filtered_traces = recording_band.get_traces(start_frame=0,
                                                                end_frame=recording_saved.get_num_samples(),
                                                                return_scaled=True)
                    frequencies, times, Zxx = stft(filtered_traces[:, i], fs=fs, nperseg=80000, noverlap=5000)
                    Zxx_db = 10 * np.log10(np.abs(Zxx) + 1e-10)
                    Zxx_db_mean = np.mean(Zxx_db)

                    results.append({'File Name': f"{folder} - {band} - Channel {i}", 'Mean': Zxx_db_mean})
                all_results.extend(results)

        except Exception as e:
            print(f"无法处理文件夹 {folder}: {e}")

    save_results_to_csv(all_results, output_file)


# 从命令行获取路径
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python Oscillation_processing.py <根文件夹路径> <输出文件夹路径>")
    else:
        base_path = sys.argv[1]
        output_folder = sys.argv[2]
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_file = os.path.join(output_folder, 'results.csv')  # 结果文件的完整路径
        process_folders(base_path, output_file)  # 传递输出文件路径
