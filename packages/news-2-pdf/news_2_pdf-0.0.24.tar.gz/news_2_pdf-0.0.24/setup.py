import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="news_2_pdf",
    version="0.0.24",
    author="Yunzhi Gao",
    author_email="gaoyunzhi@gmail.com",
    description="Generate international news in pdf.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaoyunzhi/news_2_pdf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'bs4',
        'telegram_util>=0.0.27',
        'pyyaml',
        'readee>=0.0.20',
        'link_extractor>=0.0.2',
    ],
    python_requires='>=3.0',
)