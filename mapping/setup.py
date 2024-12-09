from setuptools import setup, find_packages

setup(
    name="mapping",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "concat-files=mapping.file_concat:concat_files_with_reference",
            "process-attributes=mapping.attribute_mapping:process_attribute_mapping",
        ],
    },
)
