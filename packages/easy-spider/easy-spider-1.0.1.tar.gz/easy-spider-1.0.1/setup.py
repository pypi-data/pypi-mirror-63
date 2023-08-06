import setuptools

with open("README.md", encoding='utf-8') as fd:
    long_description = fd.read()

with open("requirements.txt", encoding="utf-8") as fd:
    install_requires = [line for line in fd.read().split("\n") if line]

setuptools.setup(
    name="easy-spider",
    version="1.0.1",
    author="lin3x",
    author_email="544670411@qq.com",
    description="A asynchronous spider with aiohttp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://lin3x.coding.net/p/easy_spider",
    packages=("easy_spider", ),
    data_files=('readme.md', 'requirements.txt'),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
