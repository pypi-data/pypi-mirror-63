#coding:utf8
'''
This is pytools moudle.
You can use tools easier than before.
About me:
Liangbob 1591609343@qq.com in China.
To take this opportunity to wish the doctor for the treatment of 2019Ncov back soon!
At The End,I wish you happy to use!
version:__version__in pytools

这是pytools模块。
您可以使用工具比以前更容易。
关于我:
中国居住 Liangbob 1591609343 @qq.com。
借此机会，祝愿最美逆行者早日回归！
最后,祝您使用愉快!
版本：pytools.__version__
'''
from pytools.error import PythonVersionErr
import platform
_python_ver=platform.python_version()
if not _python_ver.startswith('3.'):
    raise PythonVersionErr
__version__='0.0.0'

