from setuptools import setup

version = "1.0.2"
setup(
    name="zhixuewang",
    version=version,
    keywords=["智学网", "zhixue", "zhixuewang"],
    description="智学网的api",
    license="MIT",

    author="anwenhu",
    author_email="anemailpocket@163.com",

    packages=["zhixuewang", "zhixuewang.student", "zhixuewang.teacher"],
    include_package_data=True,
    platforms="any",
    install_requires=["requests"],
)
