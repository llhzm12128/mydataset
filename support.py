
import sys
sys.path.append("D:\\ISCAS\\GraduationPaper\\mydatasets\\util")
from folder_utils import FolderUtils

if __name__ == '__main__':
    dir_path = "D:\\ISCAS\\GraduationPaper\\mydatasets\\riscv_files"
    FolderUtils.get_files_count(dir_path)