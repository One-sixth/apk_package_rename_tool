# apk_package_rename_tool
APK 包名修改工具。  
APK package rename tool.  

 
# 依赖 / Dependent
python lib
```
lxml
argparse
```
不止要安装python依赖库，你还需要预先安装java运行库用来运行apktool和signapk。  
Not only python dep lib. You also need to preinstall java runtime to use apktool and signapk.  

# 如何使用 / How to use
```
下载这个储存库
安装python，python的依赖库，java运行时库
运行命令 python apk_package_rename_tool.py -i com.abc.apk -n abc.abc
输出apk文件你可以在tmp目录里面找到。

Download this repo.
Setup python, dependent lib, java runtime.
Run python apk_package_rename_tool.py -i com.abc.apk -n abc.abc
The output apk that you can found in the tmp folder.
```
