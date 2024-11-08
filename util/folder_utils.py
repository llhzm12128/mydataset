import os
import shutil

class FolderUtils(object):
    @staticmethod
    def get_subfolders(directory):
        subfolders = []
        if os.path.exists(directory) and os.path.isdir(directory):
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    subfolders.append(item_path)
        return subfolders

    def has_file(dir_path):
        with os.scandir(dir_path) as entries:
            for entry in entries:
                if (entry.is_file()):
                    return True
        return False

    def search_target_file_by_str(search_dir,search_str):
        matches = []
        for root, _, files in os.walk(search_dir):
            for file in files:
                file_path = os.path.join(root, file)

                # 打开文件并逐行搜索目标字符串
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, start=1):
                            if search_str in line:
                                # 记录匹配的文件路径和行号
                                matches.append(file_path)
                                print(f"{file_path} contains {search_str}")
                except (UnicodeDecodeError, PermissionError):
                    # 忽略不能读取的文件
                    continue

        return matches

    def copy_file_to_dir(file_path,destination_dir):
        os.makedirs(destination_dir, exist_ok=True)
        try:
            shutil.copy(file_path, destination_dir)  # 复制文件
            print(f"已复制: {file_path} -> {destination_dir}")
        except Exception as e:
            print(f"复制失败: {file_path}, 错误: {e}")

    def get_files_count(dir_path):
        file_count = sum(len(files) for _, _, files in os.walk(dir_path))
        print(f"文件夹 '{dir_path}' 中的文件数量为: {file_count}")


