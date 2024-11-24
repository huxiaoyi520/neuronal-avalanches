import os
import argparse


def rename_files(directory):
    # 遍历指定目录中的所有文件
    for filename in os.listdir(directory):
        # 检查文件是否为.mp4并且文件名中是否包含空格
        if filename.endswith(".mp4") and " " in filename:
            # 用下划线替换空格
            new_filename = filename.replace(" ", "_")
            # 获取完整的文件路径
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            # 重命名文件
            os.rename(old_file, new_file)
            print(f"重命名: {filename} -> {new_filename}")


if __name__ == "__main__":
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="批量将指定目录中.mp4文件的空格替换为下划线")
    # 添加目录路径参数
    parser.add_argument("directory", type=str, help="要处理的目录路径")
    # 解析参数
    args = parser.parse_args()

    # 运行重命名功能
    rename_files(args.directory)
# 这一行代码创建了一个 ArgumentParser 对象。
# argparse.ArgumentParser 是 Python 标准库中的一个模块，专门用来处理命令行参数。
# description 参数用于为这个脚本添加描述信息，方便用户理解这个脚本的作用。当用户运行 python rename_mp4.py --help 时，这个描述信息就会显示出来。
# add_argument 方法用于定义这个脚本所接受的参数。
# "directory" 是参数的名字。在命令行中输入的路径会被解析为这个参数的值。
# type=str 指定了这个参数的类型是字符串（路径）。
# help="要处理的目录路径" 用于提供对这个参数的帮助说明，当用户运行 python rename_mp4.py --help 时，这个说明会显示出来。

# 运行命令时，假如你输入：
#
# python rename_mp4.py /path/to/your/mp4/files
# 在代码中，/path/to/your/mp4/files 会被解析为 args.directory。
#
# args = parser.parse_args()
# 这行代码会解析命令行输入的参数，并将其存储在 args 对象中。
# args.directory 会保存用户输入的目录路径，例如 /path/to/your/mp4/files。
# 解析后的路径可以在后续代码中直接使用：
# 
# rename_files(args.directory)
# 综上，这段代码的作用是允许用户在命令行中直接指定要处理的目录，而不是在代码中硬编码路径，从而使脚本更加灵活。