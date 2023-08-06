from setuptools import setup
from os import path as os_path
from setuptools import setup

this_directory = os_path.abspath(os_path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='random_RFE',
    version='0.1.0',
    packages=['feature_selectors'],
    url='',
    install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖,
    license='MIT',
    keywords=['RFE', 'random', 'feature select'],
    author='kakarotte22',
    author_email='zhuyanfei22@icloud.com',
    description='随机递归特征消除。在使用递归特征消除的过程中，加入随机因子，根据概率随机删除特征，更大的重要性具有更小的概率被删除。',
    long_description=read_file('README.md'),  # 读取的Readme文档内容
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
)
