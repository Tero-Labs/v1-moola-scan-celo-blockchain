import setuptools

setuptools.setup(
    name="celo-sdk",
    version="1.0.0",
    description="Celo Python SDK to work with smart contracts",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
        "eth-keys==0.3.3",
        "hexbytes==0.2.1",
        "requests==2.24.0",
        "rlp==1.2.0",
        "toolz==0.10.0",
        "web3==5.12.0",
        "pycoingecko==2.0.0"
    ],
    classifiers=[
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.8",
        "Blockchain :: Celo"
    ],
    python_requires='>=3.8',
)