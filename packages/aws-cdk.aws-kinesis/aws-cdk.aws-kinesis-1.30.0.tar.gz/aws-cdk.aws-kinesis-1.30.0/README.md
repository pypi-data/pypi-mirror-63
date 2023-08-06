## Amazon Kinesis Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module.**
>
> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib))
> are auto-generated from CloudFormation. They are stable and safe to use.
>
> However, all other classes, i.e., higher level constructs, are under active development and subject to non-backward
> compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

Define an unencrypted Kinesis stream.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Stream(self, "MyFirstStream")
```

### Encryption

Define a KMS-encrypted stream:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stream = Stream(self, "MyEncryptedStream",
    encryption=StreamEncryption.Kms
)

# you can access the encryption key:
assert(stream.encryption_key instanceof kms.Key)
```

You can also supply your own key:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_kms_key = kms.Key(self, "MyKey")

stream = Stream(self, "MyEncryptedStream",
    encryption=StreamEncryption.Kms,
    encryption_key=my_kms_key
)

assert(stream.encryption_key === my_kms_key)
```
