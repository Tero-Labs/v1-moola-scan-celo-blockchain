import setuptools

setuptools.setup(
    name="celo-sdk",
    version="1.0.0",
    description="Celo Python SDK to work with smart contracts",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
        "astroid==2.4.2",
        "attrs==20.1.0",
        "autopep8==1.5.4",
        "base58==2.0.1",
        "bitarray==1.2.2",
        "certifi==2020.6.20",
        "chardet==3.0.4",
        "cmake==3.18.2.post1",
        "cytoolz==0.10.1",
        "eth-abi==2.1.1",
        "eth-account==0.5.2",
        "eth-hash==0.2.0",
        "eth-keyfile==0.5.1",
        "eth-keys==0.3.3",
        "eth-rlp==0.1.2",
        "eth-typing==2.2.1",
        "eth-utils==1.9.4",
        "hexbytes==0.2.1",
        "idna==2.10",
        "ipfshttpclient==0.6.0.post1",
        "isort==5.4.2",
        "jsonschema==3.2.0",
        "lazy-object-proxy==1.4.3",
        "lru-dict==1.1.6",
        "mccabe==0.6.1",
        "multiaddr==0.0.9",
        "netaddr==0.8.0",
        "parsimonious==0.8.1",
        "parsimonious==0.8.1",
        "py-solc==3.2.0",
        "py-solc-x==0.10.1",
        "pycodestyle==2.6.0",
        "pycryptodome==3.9.8",
        "pylint==2.6.0",
        "pyrsistent==0.16.0",
        "requests==2.24.0",
        "rlp==1.2.0",
        "semantic-version==2.8.5",
        "six==1.15.0",
        "solc==0.0.0a0",
        "toml==0.10.1",
        "toolz==0.10.0",
        "urllib3==1.25.10",
        "varint==1.0.2",
        "web3==5.12.0",
        "websockets==8.1",
        "wrapt==1.12.1",
        "uvicorn==0.12.3",
        "aiofiles==0.6.0",
        "python-multipart==0.0.5",
        "jinja2==2.11.2",
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