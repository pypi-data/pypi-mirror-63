import setuptools

long_description = """# VKBotsAPI
[![](https://img.shields.io/badge/VK-termisaal-4a76a8)](https://vk.com/termisaal)
Библиотека для работы с событиями из сообщества ВКонтакте в режиме реального времени
"""

setuptools.setup(
    name="vk-bots",
    version="0.5",
    author="Misaal",
    author_email="termisaal@gmail.com",
    description="VK API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/termisaal/VKBotsAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Natural Language :: Russian"
    ],
    python_requires='>=3.6',
)
