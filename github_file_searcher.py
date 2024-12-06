import requests
from github_repo_search import GitHubRepoSearcher
import time
import os
from pathlib import Path
import sys
import concurrent.futures  # 导入线程池相关库

sys.path.append("D:\\ISCAS\\GraduationPaper\\mydatasets\\util")
from folder_utils import FolderUtils


class GitHubFileSearcher:
    def __init__(self, token):
        """
        初始化 GitHubFileSearcher 类。

        参数:
        - token (str): GitHub 的 Personal Access Token
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def download_file(self, file_url, save_path):
        """
        下载指定 URL 的文件并保存到指定路径。

        参数:
        - file_url (str): 文件的原始 URL
        - save_path (str): 保存文件的路径
        """
        raw_url = self.construct_raw_url(file_url)
        while(True):
            response = requests.get(raw_url, headers=self.headers)
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"文件已保存到: {save_path}")
                break
            elif response.status_code == 403:
                reset_time = int(response.headers.get("X-RateLimit-Reset"))
                remaining_time = reset_time - int(time.time())
                if remaining_time > 0:
                    print(f"API 限额已用完, 请等待 {remaining_time} 秒后重新下载...")
                    time.sleep(remaining_time + 5)
                else:
                    print("配额已重置, 重新尝试请求...")
            else:
                print(f"无法下载文件: {raw_url}, 错误代码: {response.status_code}")
                break

    def search_files(self, keyword, repo_full_name, language):
        """
        在指定仓库中搜索包含特定关键字的文件。

        参数:
        - keyword (str): 搜索的关键字
        - repo_full_name (str): 仓库的全名（例如 user/repo）
        - language (str): 编程语言
        
        返回:
        - list: 包含关键字的文件列表
        """
        files = []
        page = 1
        per_page = 100

        # 构造查询 URL
        url = f"{self.base_url}/search/code?q={keyword}+in:file+language:{language}+repo:{repo_full_name}&per_page={per_page}"
        while True:
            paginated_url = f"{url}&page={page}"
            response = requests.get(paginated_url, headers=self.headers)

            # 请求成功
            if response.status_code == 200:
                data = response.json()
                print(f"page:{page}")
                items = data.get("items", [])
                if not items:
                    break  # 如果没有更多结果，退出循环

                files.extend([
                    {
                        "file_name": item["name"],
                        "file_path": item["path"],
                        "html_url": item["html_url"]
                    }
                    for item in items
                ])
                if len(items) < per_page:
                    break  # 当前页少于最大值，说明已到最后一页
                page += 1  # 请求下一页

            # 配额限制
            elif response.status_code == 403:
                reset_time = int(response.headers.get("X-RateLimit-Reset"))
                remaining_time = reset_time - int(time.time())
                if remaining_time > 0:
                    print(f"API 限额已用完, 请等待 {remaining_time} 秒后重试...")
                    time.sleep(remaining_time + 5)
                else:
                    print("配额已重置, 重新尝试请求...")
            else:
                print(f"请求失败: 仓库名：{repo_full_name},请求url:{paginated_url},{response.status_code}, {response.text}")
                break

        return files
    
    def construct_raw_url(self, html_url):
        """ 
        将 html_url 转换为 raw 内容的 URL。
        """
        if "github.com" in html_url:
            raw_url = html_url.replace("https://github.com", "https://raw.githubusercontent.com").replace("/blob/", "/")
            return raw_url
        return html_url
    
    def read_repos_from_file(self, file_path):
        """
        从文件中读取仓库名列表。

        参数:
        - file_path (str): 文件路径
        返回:
        - list: 仓库名列表
        """
        with open(file_path, 'r') as file:
            repos = [line.strip() for line in file.readlines()]
        return repos


def process_repo(repo, file_searcher, keyword):
    """处理每个仓库的搜索和下载任务"""
    files = file_searcher.search_files(keyword, repo, "c")
    if len(files) > 0:
        print(f"在仓库 {repo} 中找到包含 '{keyword}' 的文件{len(files)}个：")
        current_folder = Path(__file__).resolve().parent
        repo_folder = os.path.join(current_folder, "riscv_files")
        repo_folder = os.path.join(repo_folder, repo.replace('/', '_'))
        if not os.path.exists(repo_folder) or len(os.listdir(repo_folder)) == 0:
            os.makedirs(repo_folder, exist_ok=True)
            for file in files:
                print(f"文件名: {file['file_name']}")
                print(f"路径: {file['file_path']}")
                print(f"URL: {file['html_url']}")
                save_path = os.path.join(repo_folder, file['file_name'])
                file_searcher.download_file(file['html_url'], save_path)
            print("-" * 40)
        else:
            print(f"文件夹 {repo_folder} 已存在且非空，跳过下载。")
    else:
        print(f"在仓库 {repo} 中找不到包含 '{keyword}' 的文件。")


if __name__ == "__main__":
    token = "2"
    file_searcher = GitHubFileSearcher(token)
    keyword = "riscv_+OR+_riscv"

    # 读取仓库名列表
    repo_file_path = "repos_list.txt"
    repos = file_searcher.read_repos_from_file(repo_file_path)

    print(f"从文件中读取到 {len(repos)} 个仓库。")

    # 使用线程池优化
    with concurrent.futures.ThreadPoolExecutor(5) as executor:
        # 提交每个仓库的处理任务
        futures = [executor.submit(process_repo, repo, file_searcher, keyword) for repo in repos]

        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            pass  # 这里不需要处理返回值，因为任务本身会自动打印结果

    print("所有任务完成！")
