import logging
import gitinfo

PROGRAM_NAME = 'Psynergy'
PROGRAM_DESCRIPTION='Graphical editor for Golden Sun and other Camelot games.'
PROGRAM_VERSION = '0.0.0'

# Override PROGRAM_VERSION for local development
logging.getLogger(gitinfo.__name__).setLevel(logging.CRITICAL)
commit = gitinfo.get_git_info()
if commit is not None:
    PROGRAM_VERSION = f"dev {commit.get('author_date')} ({commit.get('commit')})"