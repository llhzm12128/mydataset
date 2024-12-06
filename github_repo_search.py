import requests
import sys
sys.path.append("D:\\ISCAS\\GraduationPaper\\mydatasets\\util")
from folder_utils import FolderUtils
import os

class GitHubRepoSearcher:
    def __init__(self, token):
        """
        初始化 GitHubRepoSearcher 类。

        参数:
        - token (str): GitHub 的 Personal Access Token
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
    
    

    def search_repos(self, query, sort="", order="desc", per_page=100):
        """
        根据查询条件搜索 GitHub 仓库，支持分页获取所有结果。

        参数:
        - query (str): 搜索关键词
        - sort (str): 排序方式，默认为按 stars 排序
        - order (str): 排序顺序，默认为降序
        - per_page (int): 每页返回的仓库数量，最大为 100

        返回:
        - list: 满足条件的仓库名称列表
        """
        all_repos = []
        page = 1

        while True:
            # 构造 URL，添加分页参数
            url = f"{self.base_url}/search/repositories?q={query}&sort={sort}&order={order}&per_page={per_page}&page={page}"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])

                # 添加当前页的结果
                all_repos.extend([repo["full_name"] for repo in items])

                # 判断是否还有更多结果
                if len(items) < per_page:
                    break  # 结束查询
                
                page += 1
            else:
                print(f"请求失败: {response.status_code}, {response.text}")
                break

        return all_repos
    
    def search_by_year(self, query, start_year, end_year, per_page=100, max_results=10000):
        """
        按时间范围分批查询仓库，获取指定年份范围内的仓库。

        参数:
        - query (str): 搜索关键词
        - start_year (int): 起始年份
        - end_year (int): 结束年份
        - per_page (int): 每页返回的仓库数量，最大为 100    
        - max_results (int): 最大结果数，默认 1000

        返回:
        - list: 满足条件的仓库名称列表
        """
        repos = []
        for year in range(start_year, end_year + 1):
            # 构建查询条件，限定时间范围
            query_first_season = f"{query} created:{year}-01-01..{year}-04-01"
            print(f"查询 {year} 年第一季度的仓库...")
            first_season_repos = self.search_repos(query_first_season, per_page=per_page)
            repos.extend(first_season_repos)
            
            query_second_season = f"{query} created:{year}-04-01..{year}-07-01"
            print(f"查询 {year} 年第二季度的仓库...")
            second_season_repos = self.search_repos(query_second_season, per_page=per_page)
            repos.extend(second_season_repos)
            
            query_third_season = f"{query} created:{year}-07-01..{year}-10-01"
            print(f"查询 {year} 年第三季度的仓库...")
            third_season_repos = self.search_repos(query_third_season, per_page=per_page)
            repos.extend(third_season_repos)
            
            query_fourth_season = f"{query} created:{year}-10-01..{year+1}-01-01"
            print(f"查询 {year} 年第四季度的仓库...")
            fourth_season_repos = self.search_repos(query_fourth_season, per_page=per_page)
            repos.extend(fourth_season_repos)

        return repos
    
    def save_repos_to_file(self, repos, file_path):
        """
        将查询到的仓库名保存到指定文件。
        参数:
        - repos (list): 仓库名列表
        - file_path (str): 文件保存路径
        """ 
        with open(file_path, 'w') as f:
            for repo in repos:
                f.write(f"{repo}\n")
        print(f"仓库名已保存到: {file_path}")


if __name__ == "__main__":

    token = "1"
    searcher = GitHubRepoSearcher(token)
    

    # 搜索含有 RISC-V 的仓库
    query = "riscv"
    repos = list(searcher.search_by_year(query, start_year=2014, end_year=2024, per_page=100))

    repo_file_path = "D:\\ISCAS\\GraduationPaper\\mydatasets\\repos_list.txt"
    searcher.save_repos_to_file(repos, repo_file_path)
    # 输出满足条件的仓库名称
    print("满足条件的仓库名称：")
    for repo_name in repos:
        print(repo_name)
    print(f"总共找到 {len(repos)} 个仓库。")
    
