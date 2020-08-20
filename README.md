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

# 注意 / Attention
该修改包名后，程序可能会不能正常工作，或部分功能受损。带有自校验和一些Kotlin编写的程序，改名后程序可能闪退，打不开，功能受损严重。  
替换包名的方式是直接替换对应的文本，没有考虑到结构问题。对一些特殊构造的包名，替换包名可能会失败。  

After the package name is modified, the program may not work normally, or some functions may be damaged. With self-checking and some programs written in Kotlin, the program may crash and fail to open after renamed, and its functions may be seriously damaged.  
The way to replace the package name is to directly replace the corresponding text, without considering the structure. For some specially constructed package names, replacing the package name may fail.  
