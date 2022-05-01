from setuptools import setup, find_packages

setup(
    name="rss_reader",
    version='0.4',
    description="Pure Python command-line RSS reader",
    author="Dauren Aidenov",
    author_email="daurenblin5@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["html_template.html", "*.jpg", "*.png", "*.css", "*.js"]
    },
    python_requires=">=3.9",
    install_requires=[
        "packaging",
        "lxml",
        "beautifulsoup4",
        "jinja2",
        "python-dateutil",
        "xhtml2pdf",
    ],
    entry_points={
        "console_scripts": ['rss_reader=src.rss_reader:main']
    }
)
