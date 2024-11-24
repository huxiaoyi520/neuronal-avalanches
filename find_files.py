##找寻文件###
import os
import shutil
import pandas as pd

# # 读取保存文件名的 CSV 文件   此处我是想把雪崩中的每组对应的15个提取出来  然后找到对应的template_metrics（里面有对应的half_width等数据 可以进行神经元分类）
# csv_file_path = r"I:\\雪崩分析\\combined_rows_control_lps7d_min7d.csv"  # 替换为你实际的 CSV 文件路径  这个就是DCC_analysis_2024_11_12.R脚本保存的对应的45个样本
# file_names_df = pd.read_csv(csv_file_path)
#
# # 提取第一列的文件名
# file_names = file_names_df.iloc[:, 1].tolist()
#
# # 替换文件名中的部分字符串
# file_names_updated = [name.replace("rhd_sorting_auto_KS25", "rhd_template_metrics") for name in file_names]
#
# # 定义查找的根目录
# source_root_folder = r"I:\intan_new"  # 替换为实际的根目录路径
#
# # 定义目标文件夹，复制到这个文件夹中
# destination_folder = r"I:\\神经元分类\\dcc\template_metrics"  # 替换为实际的目标文件夹路径
#
# # 如果目标文件夹不存在，创建它
# if not os.path.exists(destination_folder):
#     os.makedirs(destination_folder)
#
# # 遍历根目录及其子目录，寻找指定的文件
# for root, dirs, files in os.walk(source_root_folder):
#     for file in files:
#         if file in file_names_updated:  ### 如果当前文件名在要查找的文件名列表中
#             # 构建源文件和目标文件路径
#             source_file_path = os.path.join(root, file)
#             destination_file_path = os.path.join(destination_folder, file)
#
#             try:
#                 # 复制文件到当前文件夹
#                 shutil.copy2(source_file_path, destination_file_path)  ### 使用 shutil.copy2() 将源文件复制到目标文件夹中（保留元数据）
#                 print(f"Copied: {file} to {destination_folder}") ## 打印复制成功的文件信息
#             except Exception as e:
#                 print(f"Error copying {file}: {e}")
#
# print("All specified files have been copied (if found).")



##########找寻所有rhd_template_metrics.csv结尾的csv文件  然后复制到新的文件夹里面############
import os
import shutil
# 定义查找的根目录
source_root_folder = r"I:\intan_new"  # 替换为实际的根目录路径
# 定义目标文件夹，复制到这个文件夹中
destination_folder = r"I:\\神经元分类\\dcc\\template_metrics_all"  # 替换为实际的目标文件夹路径

# 如果目标文件夹不存在，创建它
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 遍历根目录及其子目录，寻找以 "rhd_template_metrics.csv" 结尾的文件
for root, dirs, files in os.walk(source_root_folder):
    for file in files:
        if file.endswith("rhd_template_metrics.csv"):  # 如果当前文件名以 "rhd_template_metrics.csv" 结尾
            # 构建源文件和目标文件路径
            source_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_folder, file)

            try:
                # 复制文件到目标位置
                shutil.copy2(source_file_path, destination_file_path)  # 使用 shutil.copy2() 将文件复制到目标文件夹中（保留元数据）
                print(f"Copied file: {file} to {destination_folder}")  # 打印复制成功的文件信息
            except Exception as e:
                print(f"Error copying file {file}: {e}")

print("All specified CSV files have been copied (if found).")





# ###找寻文件夹#####
# import os
# import shutil
# import pandas as pd
#
# # 读取保存文件名的 CSV 文件                           找寻对应的waveforms_curated文件夹 里面有firing rate等参数
# csv_file_path = r"I:\\雪崩分析\\combined_rows_control_lps7d_min7d.csv"  # 替换为你实际的 CSV 文件路径
# file_names_df = pd.read_csv(csv_file_path)
#
# # 提取第一列的文件名（文件夹名）
# file_names = file_names_df.iloc[:, 1].tolist()
#
# # 替换文件名中的部分字符串
# file_names_updated = [name.replace("rhd_sorting_auto_KS25.csv", "rhd_waveforms_curated") for name in file_names]
#
# # 定义查找的根目录
# source_root_folder = r"I:\\intan_new"  # 替换为实际的根目录路径
#
# # 定义目标文件夹，复制到这个文件夹中
# destination_folder = r"I:\\神经元分类\\dcc\waveforms_curated_all"  # 替换为实际的目标文件夹路径
#
# # 如果目标文件夹不存在，创建它
# if not os.path.exists(destination_folder):
#     os.makedirs(destination_folder)
#
# # 遍历根目录及其子目录，寻找指定的文件夹
# for root, dirs, files in os.walk(source_root_folder):
#     for folder in dirs:
#         # 如果文件夹名在文件名列表中，并以 "rhd_waveforms_curated" 结尾
#         if folder in file_names_updated and folder.endswith("rhd_waveforms_curated"):
#             # 构建源文件夹和目标文件夹路径
#             source_folder_path = os.path.join(root, folder)
#             destination_folder_path = os.path.join(destination_folder, folder)
#             try:
#                 # 复制文件夹及其所有内容到目标文件夹
#                 shutil.copytree(source_folder_path, destination_folder_path)
#                 print(f"Copied folder: {folder} to {destination_folder}")
#             except Exception as e:
#                 print(f"Error copying folder {folder}: {e}")
# print("All specified folders have been copied (if found).")


##########找寻所有rhd_waveforms_curated结尾的文件夹 然后复制到新的文件夹里
import os
import shutil

# 定义查找的根目录
source_root_folder = r"I:\intan_new"  # 替换为实际的根目录路径

# 定义目标文件夹，复制到这个文件夹中
destination_folder = r"I:\\神经元分类\\dcc\\waveforms_curated_all"  # 替换为实际的目标文件夹路径

# 如果目标文件夹不存在，创建它
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 遍历根目录及其子目录，寻找以 "rhd_waveforms_curated" 结尾的文件夹
for root, dirs, files in os.walk(source_root_folder):
    for dir_name in dirs:
        if dir_name.endswith("rhd_waveforms_curated"):  # 如果当前文件夹名以 "rhd_waveforms_curated" 结尾
            # 构建源文件夹和目标文件夹路径
            source_folder_path = os.path.join(root, dir_name)
            destination_folder_path = os.path.join(destination_folder, dir_name)

            try:
                # 复制文件夹到目标位置
                shutil.copytree(source_folder_path, destination_folder_path)  # 使用 shutil.copytree() 将整个文件夹复制到目标文件夹中
                print(f"Copied folder: {dir_name} to {destination_folder}")  # 打印复制成功的文件夹信息
            except Exception as e:
                print(f"Error copying folder {dir_name}: {e}")

print("All specified folders have been copied (if found).")




import os
import shutil
# 找寻对应的waveforms_curated文件夹 里面有firing rate等参数   把这个waveforms_curated文件夹里面的quality_metrics文件夹 里面的metrics文件 有firing rate等参数
# 定义查找的根目录
source_root_folder = r"I:\神经元分类\dcc\waveforms_curated_all"  # 你要查找的根目录路径

# 定义目标文件夹
destination_folder = r"I:\神经元分类\dcc\waveforms_curated_quality_metrics_all"  # 文件复制后的目标文件夹
# 如果目标文件夹不存在，创建它
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 遍历根目录，查找所有以 ".rhd_waveforms_curated" 结尾的文件夹
for root, dirs, files in os.walk(source_root_folder):
    for folder in dirs:
        # 如果文件夹名以 ".rhd_waveforms_curated" 结尾
        if folder.endswith(".rhd_waveforms_curated"):
            # 构建 quality_metrics 文件夹路径
            quality_metrics_folder = os.path.join(root, folder, "quality_metrics")
            metrics_file = os.path.join(quality_metrics_folder, "metrics.csv")

            # 检查 metrics.csv 文件是否存在
            if os.path.exists(metrics_file):
                # 构建新的目标文件路径，使用源文件夹名称作为文件名前缀
                new_file_name = f"{folder}_metrics.csv"
                destination_file_path = os.path.join(destination_folder, new_file_name)

                try:
                    # 复制 metrics.csv 文件到目标文件夹并重命名
                    shutil.copy2(metrics_file, destination_file_path)
                    print(f"Copied: {metrics_file} to {destination_file_path}")
                except Exception as e:
                    print(f"Error copying {metrics_file}: {e}")

print("All metrics.csv files have been copied and renamed (if found).")






import os
import pandas as pd

# 定义文件所在目录
source_folder = r"I:\神经元分类\combined_metrics_output_all"
if not os.path.exists(source_folder):
    os.makedirs(source_folder)
template_metrics_folder = r"I:\神经元分类\dcc\template_metrics_all"
if not os.path.exists(template_metrics_folder):
    os.makedirs(template_metrics_folder)
curated_metrics_folder = r"I:\神经元分类\dcc\waveforms_curated_quality_metrics_all"
if not os.path.exists(curated_metrics_folder):
    os.makedirs(curated_metrics_folder)

# 获取文件夹中的所有文件
all_template_metrics_files = os.listdir(template_metrics_folder)
all_curated_metrics_files = os.listdir(curated_metrics_folder)

# 获取以 .rhd_template_metrics.csv 和 .rhd_waveforms_curated_metrics.csv 结尾的文件
template_files = [f for f in all_template_metrics_files if f.endswith(".rhd_template_metrics.csv")]
curated_files = [f for f in all_curated_metrics_files if f.endswith(".rhd_waveforms_curated_metrics.csv")]

# 创建一个字典以便更快查找匹配的文件
curated_files_dict = {f.replace(".rhd_waveforms_curated_metrics.csv", ""): f for f in curated_files}

# 用于存储每对合并的数据
combined_dataframes = []

# 遍历所有的 .rhd_template_metrics.csv 文件，查找匹配的 .rhd_waveforms_curated_metrics.csv 文件
for template_file in template_files:
    # 获取文件的前缀部分
    base_name = template_file.replace(".rhd_template_metrics.csv", "")

    # 查找对应的 curated 文件
    if base_name in curated_files_dict:
        curated_file = curated_files_dict[base_name]

        # 构建两个文件的完整路径
        template_file_path = os.path.join(template_metrics_folder, template_file)
        curated_file_path = os.path.join(curated_metrics_folder, curated_file)

        # 读取两个 CSV 文件
        try:
            df_template = pd.read_csv(template_file_path)
            df_curated = pd.read_csv(curated_file_path)

            # 合并两个数据框，按列合并
            combined_df = pd.concat([df_template, df_curated], axis=1)

            # 将合并的数据框加入列表
            combined_dataframes.append(combined_df)

            # 保存合并后的数据框到新的 CSV 文件
            combined_file_name = f"{base_name}_combined_metrics.csv"
            combined_file_path = os.path.join(source_folder, combined_file_name)
            combined_df.to_csv(combined_file_path, index=False)
            print(f"Combined files saved as: {combined_file_name}")
        except Exception as e:
            print(f"Error reading or combining files {template_file} and {curated_file}: {e}")

print("All matching files have been combined and saved.")





import os
import pandas as pd
# 定义查找的根目录
source_folder = r"I:\神经元分类\combined_metrics_output_all"  # 替换为实际的文件夹路径

# 定义自定义的目标文件夹
destination_folder = r"I:\神经元分类\combined_metrics_output_all"  # 替换为自定义的目标文件夹路径

# 如果目标文件夹不存在，创建它
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 获取所有以 _combined_metrics.csv 结尾的文件
combined_files = [f for f in os.listdir(source_folder) if f.endswith("_combined_metrics.csv")]

# 遍历每个符合条件的文件
for file in combined_files:
    source_file_path = os.path.join(source_folder, file)

    # 读取 CSV 文件
    try:
        df = pd.read_csv(source_file_path)

        # 根据文件名添加 group 列
        if any(keyword in file for keyword in ["control"]):
            df["group"] = "control"
        elif any(keyword in file for keyword in ["lps7d", "lps_new1_7d", "lps_new2_7d", "lps_new3_7d"]):
            df["group"] = "lps7d"
        elif any(keyword in file for keyword in ["min7d", "lps_mino_new2_7d", "lps_mino_new1_7d","lps_mino_new2_7d"]):
            df["group"] = "min7d"
        elif any(keyword in file for keyword in ["lps3d", "lps_new1_3d", "lps_new2_4d","lps_new3_4d"]):
            df["group"] = "lps3d"
        else:
            print(f"Warning: No group matched for file: {file}")  # 打印出没有匹配的文件名
        # 构建目标文件路径
        destination_file_path = os.path.join(destination_folder, file)

        # 保存修改后的数据到目标文件夹中
        df.to_csv(destination_file_path, index=False)
        print(f"Updated and saved: {file} to {destination_folder}")
    except Exception as e:
        print(f"Error processing {file}: {e}")

print("All matching files have been updated and saved to the specified folder.")




import os
import pandas as pd

# 定义读取的根目录
source_folder = r"I:\神经元分类\combined_metrics_output_all"  # 替换为包含 CSV 文件的文件夹路径

# 获取所有 CSV 文件
csv_files = [f for f in os.listdir(source_folder) if f.endswith(".csv")]

# 用于存储所有文件的数据
all_dataframes = []

# 遍历每个符合条件的 CSV 文件，读取并添加到列表中
for file in csv_files:
    file_path = os.path.join(source_folder, file)

    try:
        df = pd.read_csv(file_path)
        all_dataframes.append(df)
        print(f"Loaded {file} successfully.")
    except Exception as e:
        print(f"Error reading {file}: {e}")

# 将所有数据框按行合并
combined_df = pd.concat(all_dataframes, axis=0)

# 保存合并后的数据到新的 CSV 文件中
combined_csv_path = os.path.join(source_folder, "all_combined_metrics.csv")
combined_df.to_csv(combined_csv_path, index=False)
print(f"All CSV files have been combined and saved to {combined_csv_path}.")


#
# import os
# import shutil
# def copy_preprocessed_folders(src_folder, dst_folder):
#     """
#     将源文件夹中以 .rhd_preprocessed 结尾的文件夹复制到目标文件夹中，并保持嵌套关系。
#     Parameters:
#     - src_folder: 源文件夹路径
#     - dst_folder: 目标文件夹路径
#     """
#     # 遍历源文件夹中的所有文件夹
#     for root, dirs, files in os.walk(src_folder):
#         for dir_name in dirs:
#             # 检查文件夹是否以 .rhd_preprocessed 结尾
#             if dir_name.endswith(".rhd_preprocessed"):
#                 # 获取源文件夹的完整路径
#                 src_path = os.path.join(root, dir_name)
#                 # 计算出相对于源文件夹的相对路径
#                 relative_path = os.path.relpath(src_path, src_folder)
#                 # 构建目标文件夹的完整路径
#                 dst_path = os.path.join(dst_folder, relative_path)
#
#                 # 复制文件夹及其内容到目标位置
#                 shutil.copytree(src_path, dst_path)
#                 print(f"已复制文件夹: {src_path} 到 {dst_path}")
#
#
# # 使用示例
# src_folder = r'I:\Intan'  # 源文件夹路径
# dst_folder = r'I:\各种波形分析\preprocess'  # 目标文件夹路径
#
# copy_preprocessed_folders(src_folder, dst_folder)

