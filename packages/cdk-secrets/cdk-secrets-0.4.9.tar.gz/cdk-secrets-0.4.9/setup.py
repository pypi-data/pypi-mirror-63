import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-secrets",
    "version": "0.4.9",
    "description": "CDK Construct for secrets",
    "license": "MIT",
    "url": "https://github.com/udondan/cdk-secrets",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Schroeder",
    "project_urls": {
        "Source": "https://github.com/udondan/cdk-secrets.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_secrets",
        "cdk_secrets._jsii"
    ],
    "package_data": {
        "cdk_secrets._jsii": [
            "cdk-secrets@0.4.9.jsii.tgz"
        ],
        "cdk_secrets": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.22.0",
        "publication>=0.0.3",
        "aws-cdk.aws-cloudformation>=1.24.0, <2.0.0",
        "aws-cdk.aws-iam>=1.24.0, <2.0.0",
        "aws-cdk.aws-kms>=1.24.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.24.0, <2.0.0",
        "aws-cdk.aws-s3>=1.24.0, <2.0.0",
        "aws-cdk.core>=1.24.0, <2.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
