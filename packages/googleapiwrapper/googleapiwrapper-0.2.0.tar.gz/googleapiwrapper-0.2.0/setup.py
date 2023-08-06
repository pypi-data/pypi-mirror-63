# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['googleapiwrapper']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'googleapiwrapper',
    'version': '0.2.0',
    'description': 'A simple wrapper for GoogleApi ',
    'long_description': '# TL:DR\nSimple wrapper for some of google api functions for python namely:\nGoogle Shared Drive and Google Email\n\n# How to use #\n\nExample to use the googledrivewrapper.py\n\n```python\nfrom googleapiwrapper.googledrivewrapper import GoogleSharedDrive\n\n# Load your service account credentials. Google to find out how to do it\nSERVICE_ACCOUNT_FILE = \'./credentials.json\'\n\n# instantiate the Drive\nshared_drives = GoogleSharedDrive(SERVICE_ACCOUNT_FILE)\n\n# Find the ID for the folder name\nfolder_1_id = shared_drives.fetch_folder_id(\'<YOURPROJECTNAME>\')\n\n# Create a new folder in previous folder\nnewFolder = shared_drives.create_new_folder(folder_1_id, \'<new folder>\')\n# Create another folder in new folder\'s folder\nsubfile = shared_drives.create_new_folder(newFolder[\'id\'], \'new sub folder\')\n\n# Upload a new file in new folder, will output the file meta data\nfile_metadata = shared_drives.upload_file(newFolder[\'id\'], \'./<file you need>\', \'new_file.xlsx\')\n# Get the file ID\nfileID = file_metadata.get(\'id\')\n\n# Search a file ID using file Name in a specific folder\n# You will need to provide the folder ID for this function\ninput_folder_id = "<YOURFOLDERID>"\nfile_name = "test.xlsx"\nfileID = shared_drives.search_fileID_in_folder_using_fileName(input_folder_id, file_name)\n\n# Download file from GoogleDrive\ninput_file_id = \'<YOURFOLDERID>\'\nshared_drives.download_file(input_file_id, \'./test.xlsx\')\n```\n\n\nExample to use the googleemailwrapper.py\n\n```python\nfrom googleapiwrapper.googleemailwrapper import GoogleEmail\n\nSERVICE_ACCOUNT_FILE = "./credentials.json"\nEMAIL_FROM = "<YOUREMAILADDRESS>"\nEMAIL_TO = "<OTHEREMAILADDRESS>"\nEMAIL_SUBJECT = "Hello, Test"\nEMAIL_CONTENT = "Testing. Thanks, it works"\n\n# instantiate the Email\ngmail = GoogleEmail(SERVICE_ACCOUNT_FILE, EMAIL_FROM)\n\n# Create the email contents\nmessage = gmail.create_message(EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT, [\'test.csv\'])\n\n# Send email\nsent = gmail.send_message()\n\n```\n',
    'author': 'ethan mak',
    'author_email': 'wmmak8@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wmmak12/googleapiwrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
