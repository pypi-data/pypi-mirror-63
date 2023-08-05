# sai
各种模型的实现代码

#### 安装教程
## 检查包
```angular2
python setup.py check  
```

## 生成发布软件包文件 ##
1. 安装最新版的setuptools和wheel  
```angular2
python -m pip install --user --upgrade setuptools wheel
```
1. 打包程序
```angular2
python setup.py sdist bdist_wheel
```
当这个命令运行结束后，确保在生成的dist/文件夹下存在相应的.whl文件和.tar.gz文件。其中.tar.gz文件是我们的python package的源文件文档，而.whl是一个软件分发包(build distribution)。新版本的pip将会首先尝试安装软件分发包，但在失败情况下会接着尝试采用源文件包安装。

## 本地安装包
- 安装方法1
```angular2
python setup.py build   
python setup.py install 
```
 
- 安装方法2  
```angular2
python setup.py sdist  
cd dist  
python setup.py install
```
- 安装tar.gz包  
```angular2
pip install xxx.tar.gz  
```


## 上传项目 ##
首先我们需要注册一个[PyPI](https://pypi.org/)的账号。如果仅仅为练习使用，则应当注册[test.PyPI](https://test.pypi.org/)。任何上传至test.PyPI的项目将会在一段时间之后被删除。

- upload to test PyPI  
```angular2
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

- upload to real PyPI  
```angular2
python -m twine upload dist/*
```
