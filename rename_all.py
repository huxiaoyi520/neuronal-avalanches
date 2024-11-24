import os
import argparse

def rename_files(directory):
    # 遍历指定目录中的所有文件
    for filename in os.listdir(directory):
        # 检查文件名中是否包含空格或连字符
        if " " in filename or "-" in filename:
            # 用下划线替换空格和连字符
            new_filename = filename.replace(" ", "_").replace("-", "_")
            # 获取完整的文件路径
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            # 重命名文件
            os.rename(old_file, new_file)
            print(f"重命名: {filename} -> {new_filename}")

if __name__ == "__main__":
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="批量将指定目录中所有文件的空格和连字符替换为下划线")
    # 添加目录路径参数
    parser.add_argument("directory", type=str, help="要处理的目录路径")
    # 解析参数
    args = parser.parse_args()

    # 运行重命名功能
    rename_files(args.directory)
