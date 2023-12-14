from sys import platform


project_path = ''
github_path = ''

if platform == "linux" or platform == "linux2":
    project_path = '/mnt/nas'
    github_path = '/home/aldo/github-hidrocl/HidroCL-DBCreation/'
elif platform == "darwin":
    project_path = '/private/nfs2'
    github_path = '/Users/aldotapia/Documents/GitHub/HidroCL-OOP/'


