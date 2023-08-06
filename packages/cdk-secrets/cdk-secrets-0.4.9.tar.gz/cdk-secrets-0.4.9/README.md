# DEPRECATED - CDK Secrets

This project is **deprecated**. The original goal of this construct was to provide an API for creating EC2 Key Pairs. The custom resource provider I used had much more functionality. It turned out this additional functionality was never needed and creating EC2 Key Pairs was overly complicated.

To create EC2 Key Pairs you now can use my new construct: **[cdk-ec2-key-pair](https://github.com/udondan/cdk-ec2-key-pair)**

[![CDK docs](https://img.shields.io/badge/CDK-docs-orange)](https://awscdk.io/packages/cdk-secrets@0.4.0)
[![npm version](https://badge.fury.io/js/cdk-secrets.svg)](https://www.npmjs.com/package/cdk-secrets)
[![PyPI version](https://badge.fury.io/py/cdk-secrets.svg)](https://pypi.org/project/cdk-secrets/)
[![NuGet version](https://badge.fury.io/nu/CDK.Secrets.svg)](https://www.nuget.org/packages/CDK.Secrets/)
[![GitHub](https://img.shields.io/github/license/udondan/cdk-secrets)](https://github.com/udondan/cdk-secrets/blob/master/LICENSE)

[AWS CDK](https://aws.amazon.com/cdk/) construct to manage secrets. It makes use of a custom resource provider from [binxio/cfn-secret-provider](https://github.com/binxio/cfn-secret-provider).

This package is written in TypeScript and made available via [JSII](https://github.com/aws/jsii) to all other supported languages. Package are available on:

* [npm](https://www.npmjs.com/package/cdk-secrets)
* [PyPI](https://pypi.org/project/cdk-secrets/)
* [NuGet](https://www.nuget.org/packages/CDK.Secrets/)
* [GitHub packages for Java](https://github.com/udondan/cdk-secrets/packages/99420)

The secret provider can create RSA keys, DSA keys, EC2 key-pairs, IAM user passwords and access keys and generally secrets stored in parameter store or secret store.

All this functionality is provided by the [binxio/cfn-secret-provider](https://github.com/binxio/cfn-secret-provider) custom resource.

When it comes to security, you should not trust anyone. By default the secret provider uses the lambda function stored at `s3://binxio-public-${AWS_REGION}/lambdas/cfn-secret-provider-1.0.0.zip`. You might want to download this file, review its contents and store it in your own bucket or along with your code. You then can create the lambda function from that zip file instead like so:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
code = lambda.Code.from_asset(path.join(__dirname, "../cfn-secret-provider-1.0.0.zip"))

secret_provider = secret.Provider(self, "SecretProvider",
    code=code
)
```

## Examples

There is an example application in [./example](https://github.com/udondan/cdk-secrets/blob/master/example) showing how to create a new EC2 key pair.
