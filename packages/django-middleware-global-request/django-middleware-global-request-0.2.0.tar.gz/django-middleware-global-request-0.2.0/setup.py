import os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = fobj.readlines()
requires = [x.strip() for x in requires if x.strip()]

setup(
    name="django-middleware-global-request",
    version="0.2.0",
    description="Django middleware that keep request instance for every thread.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["django extensions", "django middleware global request"],
    packages=find_packages(".", exclude=["django_middleware_global_request_example", "django_middleware_global_request_example.migrations", "django_middleware_global_request_demo"]),
    py_modules=["django_middleware_global_request"],
    requires=requires,
    install_requires=requires,
    zip_safe=False,
    include_package_data=True,
    package_data={
        "": ["*.*"],
    },
)
