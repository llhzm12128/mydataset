
import sys
sys.path.append("D:\\ISCAS\\GraduationPaper\\mydatasets\\util")
from folder_utils import FolderUtils

if __name__ == '__main__':
    riscv_files_dir  = "D:\\ISCAS\\GraduationPaper\\mydatasets\\riscv_files"
    search_folder = "D:\\ISCAS\GraduationPaper\\mydatasets\\riscv_related_open_project"
    target_string = '#include <riscv_vector.h>'
    results = FolderUtils.search_target_file_by_str(search_folder,target_string)
    for result in results:
        FolderUtils.copy_file_to_dir(result,riscv_files_dir)
    print("文件数量为："+len(results))
