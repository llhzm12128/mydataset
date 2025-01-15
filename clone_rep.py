import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
sys.path.append("/home/llh/mydataset/util")
from folder_utils import FolderUtils
from pathlib import Path
import requests




def clone_project(project_name,project_clone_path):

    print(f"git clone git@github.com:{project_name} {project_clone_path}")
    result = os.system(f"git clone git@github.com:{project_name} {project_clone_path}")
    if result != 0:
        print(f"fail to clone {project_name}")
    else:
        print(f"success clone {project_name}")


if __name__ == '__main__':

    url = "https://api.github.com/users/riscv-software-src/repos"

    # 发起请求，获取仓库数据
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        repos = response.json()
        repo_names = ["riscv-software-src/"+repo['name'] for repo in repos]  # 提取仓库名称并保存到列表
        repo_names.pop(0)
    else:
        print("Failed to fetch repositories.")

    
    project_names = ["llvm/llvm-project","gcc-mirror/gcc","OpenMathLib/OpenBLAS",
                    "tensorflow/tensorflow","pytorch/pytorch","agra-uni-bremen/riscv-vp",
                    "opencv/opencv","riscv-software-src/riscv-tests","riscv-software-src/riscv-isa-sim",
                     "riscv-collab/riscv-openocd","riscvarchive/riscv-binutils-gdb","riscv-software-src/riscv-pk"]

    repo_names1_set = set(repo_names)
    repo_names2_set = set(project_names)

    project_names_set = repo_names1_set.union(repo_names2_set)
    current_folder = Path(__file__).resolve().parent
    clone_destination_dir = os.path.join(current_folder,"downloaded_repos")
    sub_dirs = FolderUtils.get_subfolders(clone_destination_dir)

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_project = {}
        for project_name in project_names_set:
            destination_dir = os.path.join(clone_destination_dir, project_name.split("/")[-1])
            if project_name.split("/")[-1] not in sub_dirs or (not FolderUtils.has_file(destination_dir)):
                future =  executor.submit(clone_project,project_name,destination_dir)
                future_to_project[future] = project_name

        for future in as_completed(future_to_project):
            project_name = future_to_project[future]
            try:
                future.result()
            except Exception as exc:
                print(f"{project_name} generated an exception: {exc}")
    










