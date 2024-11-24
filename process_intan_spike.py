import os##用于与操作系统进行交互，如获取CPU核心数等。
from pathlib import Path  #用于处理文件路径，提供面向对象的路径操作。
import spikeinterface.full as si
from spikeinterface.extractors import read_intan  ##用于读取 Intan .rhd 格式的数据文件。
from probe_setup import create_square_probe  # 确保此脚本正确  自定义脚本，用于创建探针布局。
import numcodecs  ##用于数据压缩，如 Blosc 压缩算法。
import logging  ##用于记录日志信息，帮助调试和监控程序运行。
import traceback  ##用于捕获和格式化异常堆栈跟踪信息。
import shutil  # 用于高级文件操作，如删除文件夹。
import matplotlib.pyplot as plt
import argparse  # 用于解析命令行参数


##  tar -czvf /hy-tmp/myfolder.tar.gz myfolder/   压缩      tar -czvf /hy-tmp/min7d/lps+mino_new1_7d_241018_100600.tar.gz /hy-tmp/min7d/lps+mino_new1_7d_241018_100600/

# sudo apt-get install pigz  # 对于 Debian/Ubuntu 系统
##  tar --use-compress-program=pigz -cvf /hy-tmp/td139+3d/td139+3d.tar.gz /hy-tmp/td139+3d/



# tar：用于创建 tar 压缩包的命令。
# -c：创建新的归档文件。
# -z：使用 gzip 压缩。
# -v：显示压缩过程的详细信息。
# -f：指定输出文件名和路径（在这里为 /hy-tmp/myfolder.tar.gz）。
# myfolder/：要压缩的源文件夹。

##  oss cp oss://datasets/Intan1.rar /hy-tmp/   复制个人数据到/hy-tmp/
##  oss cp /hy-tmp/td139+3d/td139+3d.tar.gz oss://datasets/td139+3d/     复制/hy-tmp/到个人数据      find /hy-tmp/min7d/ -type f -name "*.tar.gz" -exec oss cp {} oss://datasets/min7d/ \;            find /hy-tmp/control/ -type f -name "*.tar.gz"：查找 /hy-tmp/control/ 目录下所有符合 .tar.gz 文件的路径。-exec oss cp {} oss://datasets/control/：对每个找到的 .tar.gz 文件，执行 oss cp 命令，将它们上传到 OSS 的 oss://datasets/control/ 目录。{} 会被每个文件的路径替换。\;：结束 -exec 命令
##  oss cp oss://datasets/min3d/min3d.tar.gz I:\intan_new\   复制个人数据到本地电脑  需要在oss终端使用   cp oss://datasets/lps7d/ I:\intan_new\ -r     递归下载文件夹中的所有进入本地
##                                                                                                                            find /hy-tmp/td139+3d/ -type f -name "*.tar.gz" -exec oss cp {} oss://datasets/td139+3d/ \;
##  unrar x filename.rar /hy-tmp/    解压缩

# x：表示解压到指定路径。
# /hy-tmp：目标目录。

##  rm /path/to/your/folder/*.rhd            rm /hy-tmp/control/control_new8_241011_133128/*.rhd           find /hy-tmp/td139+3d/ -type f -name "*.rhd" -exec rm -f {} \;
##  rm -r example_folder                     rm -r /hy-tmp/control/control+7_240810_112735
#   -r：表示递归删除，删除文件夹及其所有内容。


def process_rhd_file(rhd_file, input_root_folder):
    """
    处理单个 .rhd 文件的函数。

    Parameters:
    - rhd_file: Path 对象，.rhd 文件的路径。
    - input_root_folder: Path 对象，所有 .rhd 文件的根目录。
    """
    try:   #####开始一个异常捕获块，以便在整个处理过程中捕获并记录任何错误。
        # 定义文件名（不包含扩展名）作为唯一标识
        rhd_name = rhd_file.stem   ###使用 .stem 获取文件名
        # 定义相对于根目录的相对路径，用于创建唯一的输出文件夹
        relative_path = rhd_file.relative_to(input_root_folder.parent)
        # 替换路径中的分隔符为下划线，确保文件夹名称合法
        rhd_name_safe = '_'.join(relative_path.parts).replace(' ', '_').replace('+', '_')
        # 定义当前文件的基准文件夹，用于保存所有输出
        current_base_folder = rhd_file.parent
        logging.info(f"开始处理文件：{rhd_file}")
        print(f"正在处理文件：{rhd_file}")
        # 加载数据
        print("开始加载数据")
        full_raw_rec = read_intan(
            file_path=str(rhd_file),
            stream_id='0'
        )
        print("数据加载完成")
        logging.info("数据加载完成")
        # 创建探针并设置
        print("创建探针并设置")
        square_probe = create_square_probe()
        raw_rec = full_raw_rec.set_probe(square_probe)
        print("探针设置完成")
        logging.info("探针设置完成")
        # 设置脑区属性
        print("设置脑区属性")
        brain_area_property_values = ['CA1'] * square_probe.get_contact_count()
        raw_rec.set_property(key='brain_area', values=brain_area_property_values)
        print("脑区属性设置完成")
        logging.info("脑区属性设置完成")
        # 预处理步骤（带通滤波和参考）
        print("开始预处理")
        recording_f = si.bandpass_filter(raw_rec, freq_min=300, freq_max=3000)   ####检测动作电位需要这样的频率
        # 增加降噪步骤
        # recording_notch = si.notch_filter(recording_f, freq=50)  # 移除工频噪声（例如 50 Hz 或 60 Hz）
        # recording_cmr = si.common_reference(recording_f, reference='global', operator='median')
        print("预处理完成")
        logging.info("预处理完成")

        # 检测并移除坏通道
        print("检测并移除坏通道")
        bad_channel_ids, channel_labels = si.detect_bad_channels(recording_f, method='coherence+psd')  ##使用相干性和功率谱密度（PSD）方法进行坏通道检测

        recording_good_channels = recording_f.remove_channels(bad_channel_ids)  ##移除坏通道后的记录对象。
        recording_good_channels = si.common_reference(recording_good_channels, reference='global', operator='median')  ##使用全局参考。
        print("坏通道处理完成")
        logging.info("坏通道处理完成")

        # 设置并行处理参数
        job_kwargs_save = dict(n_jobs=os.cpu_count()-4, chunk_duration="1s", progress_bar=True)  ##定义一个字典，包含以下参数：n_jobs：并行处理的CPU核心数，这里设置为 1。chunk_duration：数据处理的时间块大小，这里设置为 1 秒。progress_bar：是否显示进度条，这里设置为 True。

        # 保存预处理后的数据
        print("开始保存预处理后的数据")
        preprocessed_folder = current_base_folder / f"{rhd_name_safe}_preprocessed"
        if preprocessed_folder.exists():
            shutil.rmtree(preprocessed_folder)  ###如果文件夹存在，递归删除该文件夹及其所有内容，以避免保存时冲突。
            print("已删除旧的 preprocessed 文件夹")
            logging.info("已删除旧的 preprocessed 文件夹")
        recording_saved = recording_good_channels.save(folder=preprocessed_folder
                                                       , **job_kwargs_save
                                                       )
        print("预处理后的数据保存完成")
        logging.info("预处理后的数据保存完成")

        print("开始压缩并保存数据")
        compressed_folder = current_base_folder / f"{rhd_name_safe}_preprocessed_compressed.zarr"
        if compressed_folder.exists():
            shutil.rmtree(compressed_folder)
            print("已删除旧的 preprocessed_compressed.zarr 文件夹")
            logging.info("已删除旧的 preprocessed_compressed.zarr 文件夹")
        compressor = numcodecs.Blosc(cname="zstd", clevel=9, shuffle=numcodecs.Blosc.BITSHUFFLE)   ###使用 Zstandard 压缩算法。  压缩级别，数值越高压缩越强。  数据洗牌方式，提高压缩效率。
        recording_saved = recording_good_channels.save(
            format="zarr",   ###指定保存格式为 Zarr。
            folder=compressed_folder,  ####定保存路径。
            compressor=compressor,  ###指定使用的压缩算法。
            **job_kwargs_save
        )
        print("压缩数据保存完成")
        logging.info("压缩数据保存完成")

        # 运行排序器（例如 SpyKING CIRCUS 2）
        print("开始运行排序器")
        sorting_output_folder = current_base_folder / f"{rhd_name_safe}_results_SC2"
        if sorting_output_folder.exists():
            shutil.rmtree(sorting_output_folder)
            print("已删除旧的 results_SC2 文件夹")
            logging.info("已删除旧的 results_SC2 文件夹")
        sorting_SC2 = si.run_sorter(
            'spykingcircus2',
            recording_saved,
            output_folder=sorting_output_folder,
            verbose=True,  ###启用详细输出，显示排序过程中的详细信息。
            # 不传递 job_kwargs_save
            job_kwargs=job_kwargs_save
        )
        print("排序器运行完成")
        logging.info("排序器运行完成")

        # 提取波形
        print("开始提取波形")
        waveforms_folder = current_base_folder / f"{rhd_name_safe}_waveforms_dense"
        we = si.extract_waveforms(
            recording_saved,
            sorting_SC2,
            folder=waveforms_folder,
            sparse=False,
            overwrite=True,
            allow_unfiltered=True,
            **job_kwargs_save
        )
        print("波形提取完成")
        logging.info("波形提取完成")

        # 打印一些波形信息
        waveforms0 = we.get_waveforms(unit_id=0)
        print(f"Waveforms shape: {waveforms0.shape}")
        template0 = we.get_template(unit_id=0)
        print(f"Template shape: {template0.shape}")
        all_templates = we.get_all_templates()
        print(f"All templates shape: {all_templates.shape}")
        for unit in sorting_SC2.get_unit_ids():
            waveforms = we.get_waveforms(unit_id=unit)
            spiketrain = sorting_SC2.get_unit_spike_train(unit)
            print(f"Unit {unit} - num waveforms: {waveforms.shape[0]} - num spikes: {len(spiketrain)}")

        # 计算稀疏性
        print("开始计算稀疏性")
        sparsity = si.compute_sparsity(we, method='radius', radius_um=12.5)
        print("稀疏性计算完成")
        logging.info("稀疏性计算完成")

        # 检查稀疏性
        print("检查稀疏性")
        for unit_id in sorting_SC2.unit_ids:
            print(unit_id, list(sparsity.unit_id_to_channel_ids[unit_id]))

        # 提取稀疏波形
        print("开始提取稀疏波形")
        waveforms_sparse_folder = current_base_folder / f"{rhd_name_safe}_waveforms_sparse_explicit"
        if waveforms_sparse_folder.exists():
            shutil.rmtree(waveforms_sparse_folder)
            print("已删除旧的 waveforms_sparse_explicit 文件夹")
            logging.info("已删除旧的 waveforms_sparse_explicit 文件夹")
        we_sparse = si.extract_waveforms(
            recording_saved,
            sorting_SC2,
            folder=waveforms_sparse_folder,
            sparsity=sparsity,
            allow_unfiltered=True,
            overwrite=True,
            **job_kwargs_save
        )
        print("稀疏波形提取完成")
        logging.info("稀疏波形提取完成")

        # 计算主成分
        print("开始计算主成分")
        pc = si.compute_principal_components(
            we_sparse,
            n_components=3,
            load_if_exists=False,
            **job_kwargs_save
        )
        print("主成分计算完成")
        logging.info("主成分计算完成")

        # 打印主成分信息
        pc0 = pc.get_projections(unit_id=0)
        print(f"PC scores shape: {pc0.shape}")
        all_labels, all_pcs = pc.get_all_projections()
        print(f"All PC scores shape: {all_pcs.shape}")

        # 计算峰值幅度
        print("开始计算峰值幅度")
        amplitudes = si.compute_spike_amplitudes(
            we_sparse,
            outputs="by_unit",
            load_if_exists=True,
            **job_kwargs_save
        )
        print("峰值幅度计算完成")
        logging.info("峰值幅度计算完成")

        # 计算单位位置
        print("开始计算单位位置")
        unit_locations = si.compute_unit_locations(
            we_sparse,
            method="monopolar_triangulation",
            load_if_exists=True
        )
        spike_locations = si.compute_spike_locations(
            we_sparse,
            method="center_of_mass",
            load_if_exists=True,
            **job_kwargs_save
        )
        print("单位位置计算完成")
        logging.info("单位位置计算完成")

        # 计算质量指标
        print("开始计算质量指标")
        metric_names = si.get_quality_metric_list()
        qm_params = si.get_default_qm_params()
        qm = si.compute_quality_metrics(
            we_sparse,
            metric_names=metric_names,
            verbose=True,
            qm_params=qm_params,
            **job_kwargs_save
        )

        print("质量指标计算完成")
        logging.info("质量指标计算完成")

        # 应用质量指标筛选
        print("开始应用质量指标筛选")
        isi_viol_thresh = 1.5
        amp_cutoff_thresh = 0.1
        our_query = f"amplitude_cutoff < {amp_cutoff_thresh} & isi_violations_ratio < {isi_viol_thresh}"

        keep_units = qm.query(our_query)
        keep_unit_ids = keep_units.index.values
        sorting_auto_KS25 = sorting_SC2.select_units(keep_unit_ids)

        print("质量指标筛选完成")
        logging.info("质量指标筛选完成")

        # 保存整理后的结果
        print("开始保存整理后的结果")
        waveforms_curated_folder = current_base_folder / f"{rhd_name_safe}_waveforms_curated"
        if waveforms_curated_folder.exists():
            shutil.rmtree(waveforms_curated_folder)
            print("已删除旧的 waveforms_curated 文件夹")
            logging.info("已删除旧的 waveforms_curated 文件夹")
        we_curated = we_sparse.select_units(
            keep_unit_ids,
            new_folder=waveforms_curated_folder
        )
        sorting_auto_KS25.save(folder=current_base_folder / f"{rhd_name_safe}_sorting_auto_KS25")
        print("整理后的结果保存完成")
        logging.info("整理后的结果保存完成")

        # 计算模板相似度和指标
        print("开始计算模板相似度和指标")
        similarity = si.compute_template_similarity(we_curated)
        template_metrics = si.compute_template_metrics(
            we_curated,
            upsampling_factor=3
        )
        print("模板相似度和指标计算完成")
        logging.info("模板相似度和指标计算完成")

        # 保存 template_metrics 到 CSV 文件
        print("开始保存 template_metrics 到 CSV 文件")
        template_metrics_file = current_base_folder / f"{rhd_name_safe}_template_metrics.csv"
        template_metrics.to_csv(template_metrics_file, index=False)
        logging.info(f"模板指标已保存到 {template_metrics_file}")
        print("template_metrics 保存完成")
        print(f"文件 {rhd_file} 的处理完成，结果已保存到 {current_base_folder}")
        logging.info(f"文件 {rhd_file} 的处理完成，结果已保存到 {current_base_folder}")

    except Exception as e:
        error_message = traceback.format_exc()
        print(f"处理文件 {rhd_file} 时出错：{e}")
        print(error_message)
        logging.error(f"处理文件 {rhd_file} 时出错：{e}\n{error_message}")

def main():

    # 设置根目录
    input_root_folder = Path(r'/hy-tmp/td139+3d/td139+4d+3_240904_131156')#########更换成云服务器的路径   td139+4d+3_240904_131156

    # 设置日志记录
    logging.basicConfig(   ###配置日志记录：
        filename=input_root_folder / 'processing.log',   ###日志文件的保存路径，
        level=logging.INFO,   ###日志级别设置为 INFO，表示记录所有级别高于或等于 INFO 的日志信息
        format='%(asctime)s - %(levelname)s - %(message)s'   ###志信息的格式，包含时间、日志级别和消息内容。
    )

    # 查找所有 .rhd 文件
    rhd_files = list(input_root_folder.rglob('*.rhd'))

    # 检查是否找到任何 .rhd 文件
    if not rhd_files:
        print("在指定的输入文件夹及其子文件夹中未找到任何 .rhd 文件。")
        logging.info("未找到任何 .rhd 文件。")
        return
    else:
        print(f"找到 {len(rhd_files)} 个 .rhd 文件。")
        logging.info(f"找到 {len(rhd_files)} 个 .rhd 文件。")

    # 设置并行处理参数
    n_cpus = os.cpu_count()
    n_jobs = max(1, n_cpus - 4)  # 确保至少使用1个CPU
    print(f"使用 {n_jobs} 个 CPU 核心进行处理。")
    logging.info(f"使用 {n_jobs} 个 CPU 核心进行处理。")

    # 遍历每个 .rhd 文件，进行处理
    for rhd_file in rhd_files:
        process_rhd_file(rhd_file, input_root_folder)

# def main():
#     # 设置命令行参数解析
#     parser = argparse.ArgumentParser(description="批量处理电生理 .rhd 数据文件。")
#     parser.add_argument('folder', type=str, help="要处理的根文件夹路径。")
#     args = parser.parse_args()
#     # 设置根目录
#     input_root_folder = Path(args.folder)
#     # 验证输入文件夹是否存在
#     if not input_root_folder.exists() or not input_root_folder.is_dir():
#         print(f"指定的文件夹 {input_root_folder} 不存在或不是一个目录。")
#         return
#
#     # 设置日志记录
#     logging.basicConfig(  ###配置日志记录：
#         filename=input_root_folder / 'processing.log',  ###日志文件的保存路径，
#         level=logging.INFO,  ###日志级别设置为 INFO，表示记录所有级别高于或等于 INFO 的日志信息
#         format='%(asctime)s - %(levelname)s - %(message)s'  ###志信息的格式，包含时间、日志级别和消息内容。
#     )
#
#     # 查找所有 .rhd 文件
#     rhd_files = list(input_root_folder.rglob('*.rhd'))
#
#     # 检查是否找到任何 .rhd 文件
#     if not rhd_files:
#         print("在指定的输入文件夹及其子文件夹中未找到任何 .rhd 文件。")
#         logging.info("未找到任何 .rhd 文件。")
#         return
#     else:
#         print(f"找到 {len(rhd_files)} 个 .rhd 文件。")
#         logging.info(f"找到 {len(rhd_files)} 个 .rhd 文件。")
#
#     # # 设置并行处理参数
#     # n_cpus = os.cpu_count()
#     # n_jobs = max(1, n_cpus - 4)  # 确保至少使用1个CPU
#     # print(f"使用 {n_jobs} 个 CPU 核心进行处理。")
#     # logging.info(f"使用 {n_jobs} 个 CPU 核心进行处理。")
#
#     # 遍历每个 .rhd 文件，进行处理
#     for rhd_file in rhd_files:
#         process_rhd_file(rhd_file, input_root_folder
#                          # , n_jobs=n_jobs
#                          )


if __name__ == "__main__":
    main()

# 假设您的脚本名称为 process_intan.py，您可以按照以下方式在Anaconda Prompt中运行：
# python process_intan.py "I:\test" --jobs 4  可选参数，指定使用4个CPU核心进行处理。如果未指定，默认为1。
