# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['httpie_nifcloud_authv4']
install_requires = \
['aws-requests-auth>=0.4.2,<0.5.0', 'httpie>=2.0.0,<3.0.0']

entry_points = \
{'httpie.plugins.auth.v1': ['httpie_aws_authv4 = '
                            'httpie_nifcloud_authv4:AWSv4AuthPlugin',
                            'httpie_nifcloud_authv4 = '
                            'httpie_nifcloud_authv4:NIFCLOUDv4AuthPlugin']}

setup_kwargs = {
    'name': 'httpie-nifcloud-authv4',
    'version': '0.1.0',
    'description': 'AWS/NIFCLOUD Auth v4 plugin for HTTPie',
    'long_description': 'httpie-nifcloud-authv4\n======================\n\nAWS/NIFCLOUD Auth v4 plugin for HTTPie\n\nDescription\n-----------\n\n`HTTPie <https://httpie.org>`__ で AWS / NIFCLOUD Signature v4\nの認証をリクエストに付加するための Auth plugin です。\n\nInstall\n-------\n\n.. code:: bash\n\n   pip install --upgrade httpie-nifcloud-authv4\n\ngithub masterからinstallする場合:\n\n.. code:: bash\n\n   pip install --upgrade git+https://github.com/kzmake/httpie-nifcloud-authv4\n\nPreparation\n-----------\n\n``-A nifcloud`` の場合、 1. ``-a ...`` で指定された\n``ACCESS_KEY_ID / SECRET_ACCESS_KEY`` 1. 環境変数\n``NIFCLOUD_ACCESS_KEY_ID / NIFCLOUD_SECRET_ACCESS_KEY`` 2. 環境変数\n``ACCESS_KEY_ID / SECRET_ACCESS_KEY``\n\nの順で適用されます。\n\n環境変数 ACCESS_KEY_ID / SECRET_ACCESS_KEY を用いてリクエストする場合\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nfor bash / zsh\n\n.. code:: bash\n\n   export ACCESS_KEY_ID={払い出されたACCESS_KEY_ID}\n   export SECRET_ACCESS_KEY={払い出されたSECRET_ACCESS_KEY}\n\nfor fish\n\n.. code:: fish\n\n   set -gx ACCESS_KEY_ID {払い出されたACCESS_KEY_ID}\n   set -gx SECRET_ACCESS_KEY {払い出されたSECRET_ACCESS_KEY}\n\nACCESS_KEY_ID / SECRET_ACCESS_KEY を設定後、リクエストしてください。\n\nリクエストに直接 ACCESS_KEY_ID / SECRET_ACCESS_KEY を指定してリクエストする場合\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n.. code:: bash\n\n   http -v -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY} https://jp-east-1.hatoba.api.nifcloud.com/v1/clusters\n\n上記のコマンドのように\n``-a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY}``\nを追加してリクエストしてください。\n\nUsage\n-----\n\n``-A nifcloud`` を HTTPie に追加し、リクエストしてください。\n\n利用可能な引数の形式\n~~~~~~~~~~~~~~~~~~~~\n\n``-a ...`` で認証情報を指定することが可能です。\\ ``...``\nに指定可能な形式は以下となります。\n\n-  {region_name}/{service_id}\n-  {ACCESS_KEY_ID}:{SECRET_ACCESS_KEY}\n-  {ACCESS_KEY_ID}:{SECRET_ACCESS_KEY}:{region_name}/{service_id}\n-  {ACCESS_KEY_ID}:{SECRET_ACCESS_KEY}:{region_name}:{service_id}\n\n{region_name}.{service_name}.api.nifcloud.com の場合\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n-  オブジェクトストレージ\n-  Hatoba（β）\n-  NAS\n-  RDB\n\n``{region_name}`` / ``{service_id}`` に ``.``\nが含まれない場合、自動でregion_name/service_idを読み取りリクエストします。\nまたは、\\ ``-a {region_name}/{service_id}``\nと指定し、リクエストしてください。\n\n.. code:: bash\n\n   http -v -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY} https://jp-east-1.hatoba.api.nifcloud.com/v1/clusters\n\n   http -v -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY}:jp-east-1/hatoba https://jp-east-1.hatoba.api.nifcloud.com/v1/clusters\n\n   http -v -A nifcloud -a jp-east-1/hatoba https://jp-east-1.hatoba.api.nifcloud.com/v1/clusters\n\n{service_name}.api.nifcloud.com の場合\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n-  ESS\n-  スクリプト\n\n``-a /{service_id}`` と指定し、リクエストしてください。\n\n.. code:: bash\n\n   http -v -f -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY}:east-1/email https://ess.api.nifcloud.com/ Action=ListIdentities Version=2010-12-01\n\n   http -v -f -A nifcloud -a east-1/email https://ess.api.nifcloud.com/ Action=ListIdentities Version=2010-12-01\n\nGET の例\n~~~~~~~~\n\nQuery (``Action==ListIdentities Version=2010-12-01``)\nを指定してリクエストしてください。\n\n.. code:: bash\n\n   http -v -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY}:east-1/email https://ess.api.nifcloud.com/ Action==ListIdentities Version==2010-12-01\n\nPOST の例\n~~~~~~~~~\n\nFormオプション(``-f``) を指定し、 Form data\n(``Action=ListIdentities Version=2010-12-01``)\nを指定してリクエストしてください。\n\n.. code:: bash\n\n   http -v -f -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY}:east-1/email https://ess.api.nifcloud.com/ Action=ListIdentities Version=2010-12-01\n\nraw-payload(``"Action=ListIdentities&Version=2010-12-01"``)\nをパイプで渡してリクエストする場合は以下のようになります。\n\n.. code:: bash\n\n   printf "Action=ListIdentities&Version=2010-12-01" | http -v -f -A nifcloud -a east-1/email https://ess.api.nifcloud.com/\n\n   echo "Action=ListIdentities&Version=2010-12-01" | tr -d \'\\n\' | http -v -f -A nifcloud -a east-1/email https://ess.api.nifcloud.com/\n\n',
    'author': 'kzmake',
    'author_email': 'kzmake.i3a@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kzmake/httpie-nifcloud-authv4',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
