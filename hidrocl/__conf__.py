from sys import platform


project_path = ''
github_path = ''
observed_products_path = 'observed'
forecasted_products_path = 'forecasted'
processing_path = ''

if platform == "linux" or platform == "linux2":
    project_path = '/mnt/nas'
    processing_path = '/mnt/nas/'
    github_path = '/home/aldo/github-hidrocl/HidroCL-DBCreation/'
elif platform == "darwin":
    project_path = '/private/nfs2'
    processing_path = '/private/nfs2'
    github_path = '/Users/aldotapia/Documents/GitHub/HidroCL-OOP/'


