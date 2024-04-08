from sys import platform
from dotenv import load_dotenv

if platform == "linux" or platform == "linux2":
    project_path = '/mnt/nas'
    processing_path = '/mnt/nas/'
    github_path = '/home/aldo/github-hidrocl/HidroCL-DBCreation/'
elif platform == "darwin":
    project_path = '/private/nfs2'
    processing_path = '/private/nfs2'
    github_path = '/Users/aldotapia/Documents/GitHub/HidroCL-OOP/'

def set_env(path = '.env'):
    """
    Set the environment variables

    Args:
        path (str): path to the .env file

    Returns:
        None
    """
    # check if the path exists
    global project_path, github_path, observed_products_path, forecasted_products_path,\
        processing_path, hidrocl_root_path, report_emails

    if not os.path.exists(path):
        project_path = ''
        github_path = ''
        observed_products_path = ''
        forecasted_products_path = ''
        processing_path = ''
        hidrocl_root_path = ''
        report_emails = ['']

    else:

        load_dotenv(path)
        # check if the environment variables exists from the .env file
        if 'PROJECT_PATH' not in os.environ:
            raise KeyError('PROJECT_PATH not found in .env file')
        if 'GITHUB_PATH' not in os.environ:
            raise KeyError('GITHUB_PATH not found in .env file')
        if 'OBSERVED_PRODUCTS_PATH' not in os.environ:
            raise KeyError('OBSERVED_PRODUCTS_PATH not found in .env file')
        if 'FORECASTED_PRODUCTS_PATH' not in os.environ:
            raise KeyError('FORECASTED_PRODUCTS_PATH not found in .env file')
        if 'PROCESSING_PATH' not in os.environ:
            raise KeyError('PROCESSING_PATH not found in .env file')
        if 'HIDROCL_ROOT_PATH' not in os.environ:
            raise KeyError('HIDROCL_ROOT_PATH not found in .env file')
        project_path = os.environ['PROJECT_PATH']
        github_path = os.environ['GITHUB_PATH']
        observed_products_path = os.environ['OBSERVED_PRODUCTS_PATH']
        forecasted_products_path = os.environ['FORECASTED_PRODUCTS_PATH']
        processing_path = os.environ['PROCESSING_PATH']
        hidrocl_root_path = os.environ['HIDROCL_ROOT_PATH']
        report_emails = os.environ['REPORT_EMAILS'].split(',')

    return None


