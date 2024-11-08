import requests
from bs4 import BeautifulSoup
import os
import shutil



# GitHub Trending URLs
GITHUB_TRENDING_URLS = {
    "daily": "https://github.com/trending/c?since=daily",
    "weekly": "https://github.com/trending/c?since=weekly",
    "monthly": "https://github.com/trending/c?since=monthly"
}


def get_trending_c_projects():
    projects = {}

    for period, url in GITHUB_TRENDING_URLS.items():
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve {period} trending projects")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Collect all project links for the period
        for repo in soup.find_all('h2', class_='h3 lh-condensed'):
            a_tag = repo.find('a')
            project_name = a_tag.text.strip().replace(" ", "").replace("\n", "")
            project_url = "https://github.com" + a_tag['href']
            projects[project_name] = project_url  # 去重：使用项目名称作为键存储唯一项目

    return list(projects.items())


def clone_project(project_url,project_clone_path):

    print(f"git clone {project_url} {project_clone_path}")
    os.system(f"git clone {project_url} {project_clone_path}")


def has_file(dir_path):
    with os.scandir(dir_path) as entries:
        for entry in entries:
            if(entry.is_file()):
                return True
    return False





def get_sub_dir(dir_path):
    sub_dirs = []
    sub_file_and_dirs = os.listdir(dir_path)
    for sub_file_and_dir in sub_file_and_dirs:
        if os.path.isdir(os.path.join(source_directory, sub_file_and_dir)):
            sub_dirs.append(sub_file_and_dir)
    return sub_dirs

def clone_c_files(source_directory, destination_directory):
    os.makedirs(destination_directory, exist_ok=True)
    # 遍历源文件夹及其所有子文件夹
    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            if filename.endswith('.c'):  # 过滤 .c 文件
                # 构建源文件的完整路径
                source_file = os.path.join(root, filename)
                # 构建目标文件的完整路径
                destination_file = os.path.join(destination_directory, filename)

                # 防止文件重名覆盖
                if not os.path.exists(destination_file):
                    shutil.copy(source_file, destination_file)

    print("所有 .c 文件已成功复制到目标文件夹。")


if __name__ == "__main__":
    # 目标目录，用于存储克隆的项目和 .c 文件
    current_folder = Path(__file__).resolve().parent
    source_directory = os.path.join(current_folder,"cdataset")

    destination_directory = os.path.join(current_folder,"c_files")

    # 获取去重后的 trending 项目
    trending_c_projects = get_trending_c_projects()
    print("Unique Trending C Language Projects:")
    sub_dirs = get_sub_dir(source_directory)
    for project_name, project_url in trending_c_projects:

        print(f"- {project_name}: {project_url}")
        project_clone_path = os.path.join(source_directory, project_name.split("/")[-1]).replace("/","\\")

        if project_name.split("/")[-1] not in sub_dirs or (not has_file(project_clone_path)) :
            print(f"git clone git@github.com:{project_name}.git {project_clone_path}")
            os.system(f"git clone git@github.com:{project_name}.git {project_clone_path}")
            #clone_project(project_url,project_clone_path)

    # 从克隆的项目中提取 .c 文件
    clone_c_files(source_directory, destination_directory)

    # 输出 .c 文件数量
    file_count = sum(len(files) for _, _, files in os.walk(destination_directory))
    print(f"文件夹 '{destination_directory}' 中的 .c 文件数量为: {file_count}")
