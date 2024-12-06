import requests
import sys
sys.path.append("D:\\ISCAS\\GraduationPaper\\mydatasets\\util")
from folder_utils import FolderUtils

if __name__ == '__main__':
    dir_path = "D:\\ISCAS\\GraduationPaper\\mydatasets\\riscv_files"
    FolderUtils.get_files_count(dir_path)
    
    token = "1"
    headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    url = "https://api.github.com/search/repositories?q=riscv&page=1&per_page=100"
    response = requests.get(url, headers=headers)
    
