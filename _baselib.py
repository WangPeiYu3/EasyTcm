import os

import zipfile

import os


def count_files_in_directory(directory_path):
    try:
        # 列出目录下所有文件和子目录，并过滤出文件
        only_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        return len(only_files)
    except FileNotFoundError:
        print(f"目录 {directory_path} 不存在")
        return 0
    except PermissionError:
        print(f"没有权限访问目录 {directory_path}")
        return 0
    except Exception as e:
        print(f"发生错误: {e}")
        return 0


def zip_dir(directory, output_filename):
    # 创建一个ZipFile对象，并设置压缩模式为ZIP_DEFLATED
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历指定目录下的所有文件
        for root, dirs, files in os.walk(directory):
            for file in files:
                # 构建完整的路径，并添加到ZIP文件中
                filepath = os.path.join(root, file)
                # 使用arcname参数来避免在ZIP文件中包含完整的路径信息
                arcname = os.path.relpath(filepath, start=os.path.dirname(directory))
                zipf.write(filepath, arcname=arcname)


def split_path_os(filepath):
    # 将路径转为绝对路径
    abs_filepath = os.path.abspath(filepath)
    # 分离文件路径和文件名
    path, filename = os.path.split(abs_filepath)
    return path, filename


def move_xlsx_to_result_folder(src_folder='.', dst_folder='result'):
    import shutil

    """
    将源文件夹中的所有.xlsx文件移动到目标文件夹。

    参数:
        src_folder (str): 源文件夹路径，默认为当前文件夹 ('.')。
        dst_folder (str): 目标文件夹路径，默认为 'result'。
    """
    # 确保目标文件夹存在，如果不存在则创建
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
        print(f"创建了新的文件夹: {dst_folder}")

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(src_folder):
        # 检查文件是否为.xlsx文件
        if filename.endswith('.xlsx') or filename.endswith('.png'):
            src_file = os.path.join(src_folder, filename)
            dst_file = os.path.join(dst_folder, filename)

            # 如果目标文件已存在，则避免覆盖，可以添加编号或其他方式处理
            if os.path.exists(dst_file):
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(os.path.join(dst_folder, f"{base}_{counter}{ext}")):
                    counter += 1
                dst_file = os.path.join(dst_folder, f"{base}_{counter}{ext}")
                print(f"目标文件已存在，重命名为: {os.path.basename(dst_file)}")

            # 移动文件
            shutil.move(src_file, dst_file)
            print(f"已移动文件: {filename} 到 {dst_folder}")


import os


def modify_file_name(directory='', prefix='step2.四气、五味、归经、治法属性转换_', replace_prefix='step4.统计矩阵'):
    # 获取目录下的所有条目
    entries = os.listdir(directory)
    # 过滤出只包含文件并且文件名以指定前缀开头的列表
    files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry)) and entry.startswith(prefix)]

    for file_name in files:
        new_file_name = file_name.replace(prefix, replace_prefix, 1)  # 确保只替换最前面的一个匹配
        old_path = os.path.join(directory, file_name)
        new_path = os.path.join(directory, new_file_name)

        # 如果新文件名已存在，则先删除它
        if os.path.exists(new_path):
            os.remove(new_path)

        # 重命名文件
        os.rename(old_path, new_path)

    return files  # 返回被重命名的文件列表
