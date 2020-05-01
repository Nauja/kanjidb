import io
from setuptools import setup


def readme():
    with open("README.rst") as f:
        return f.read()


def read(*filenames, **kwargs):
    ''' Read contents of multiple files and join them together '''
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


pkg_info = {}
exec(read('kanjidb/__version__.py'), pkg_info)


setup(
    name="kanjidb",
    version=pkg_info['__version__'],
    description="Kanji Database",
    long_description=readme(),
    packages=[
        "kanjidb",
        "kanjidb.builder",
        "kanjidb.builder.plugins",
        "kanjidb.service"
    ],
    test_suite="nose.collector",
    tests_require=["nose", "nose-cover3"],
    include_package_data=True,
    zip_safe=False,
)
