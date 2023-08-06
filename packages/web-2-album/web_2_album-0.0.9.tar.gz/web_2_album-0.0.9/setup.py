import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="web_2_album",
    version="0.0.9",
    author="Yunzhi Gao",
    author_email="gaoyunzhi@gmail.com",
    description="Return photo list and caption (markdown format) from web.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaoyunzhi/web_2_album",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'cached_url >= 0.0.6'
        'bs4',
        'telegram_util >= 0.0.37',
        'pic_cut >= 0.0.8',
        'readee >= 0.0.24',
        'export_to_telegraph >= 0.0.45'
    ],
    python_requires='>=3.0',
)