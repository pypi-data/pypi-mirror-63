# THIS REPOSITORY IS A WORK IN PROGRESS
**IF YOU SEE THIS MESSAGE DO NOT UNDER ANY CIRCUMSTANCE DELETE INFRASTRUCTURE HOPING THAT WINTERGREEN CAN REBUILD IT**
We're working on it.


## Purpose

The responsibility of Wintergreen is to create and manage client-side SSL certificates for authenticating IoT devices with cloud services.

Automate device registry in AWS IoT because it sucks. `wintergreen` is a command line utility that provides mechanisms to automate cumbersome tasks related to signing and registering AWS IoT Thing device certificates.


### What it does

Provide a quick way to develop with a security-first mindset regarding your IoT web infrastructure by allowing you to avoid the hassle of generating and certs and associating them with your infrastructure

### What it doesn't do

Provide a secure pattern for managing device certificates in a hardware production setting.  It does not give you a secure means for allowing a third party manufacturer to generate and/or load certificates onto hardware.

## Requirements
As Wintergreen manipulates AWS resources, an AWS account is required.

Wintergreen leverages boto3 and acts on the users behalf to create and manipulate resources in AWS.
The user should have AWS credentials set in their environment. In order to check this, you might use the AWS CLI and run `aws sts get-caller-identity`. This is the user wintergreen will leverage.

## Installing the CLI
`pip install wintergreen`

## Run

## Initialize
Initialization means
- Creating a ThingType
- Creating a RootCA cert/key pair
- Registering that RootCA with AWS
- Creating a Just-in-time Provisioning role

Example:
`poetry run wintergreen init -t my-cool-thing`
Check your `~/.wintergreen` directory to see a subdirectory for `my-cool-thing`

```bash
$  wintergreen init --help
Usage: wintergreen init [OPTIONS]

Options:
  -t, --thing-type TEXT       AWS IoT thing type  [required]
  -p, --platform [aws|local]  Platform to upload root CA  [required]
  -a, --algorithm [rsa|ec]    Encryption algorithms supported  [required]
  -c, --country TEXT          Country code (2-letter) to use for provisioning
                              certs i.e. US  [required]
  -f, --fqdn TEXT             Domain of the organization to use in the CA e.g.
                              verypossible.com
  -o, --organization TEXT     Organization name i.e. Very
  -s, --state TEXT            State or Province code (2-letter) to use for
                              provisioning certs i.e. TN
  -l, --locality TEXT         Locality to use for provisioning certs i.e.
                              Chattanooga
  -u, --unit TEXT             Organizational unit to use for provisioning
                              certs i.e. Engineering
  -d, --days INTEGER          Days until CA will expire  [default: 365]
  -k, --key-size INTEGER      [default: 2048]
  --help                      Show this message and exit.

Outputs:
{
    "platform_response": {
        "thingTypeName": "thing_type",
        "thingTypeArn": "arn:aws:iot:us-east-1:...",
        "thingTypeId": "...",
        "jitpRoleArn": "arn:aws:iam::...",
        "certificateArn": "arn:aws:iot:us-east-1:..."
    },
    "success": true,
    "platform": "aws"
}
```

## Provision a new device

Provisioning a device means generating a certificate/key pair to be used for the device to authenticate with AWS IoT.

```bash
$ wintergreen provision --help
Usage: wintergreen provision [OPTIONS]

Options:
  -t, --thing-type TEXT    Same as the thing-type that was chosen in the
                           `init` step.
  -cn, --common_name TEXT  Defaults to a UUIDv4
  -c, --country TEXT       [required]
  -o, --organization TEXT
  -s, --state TEXT
  -l, --locality TEXT
  -u, --unit TEXT
  -d, --days INTEGER       Days until certificate will expire  [default: 365]
  -k, --key-size INTEGER   [default: 2048]
  -n, --number INTEGER     Number of certificates to provision  [default: 1]
  -v, --verbosity          Verbosity, add v's for more.
  --help                   Show this message and exit.

Outputs (depends on verbosity):
common_name1
common_name2
Generated 2 certificate(s)
```

These will be written as files scoped by date into your `.wintergreen` directory. If you use the `-n` argument, it will generate a unique uuid for each cert and put all of the certs generated in their own folder. You'll also see an output.csv which contains a table of all the certs generated on this run.

## Verifying if your provisioned cert can connect
After running the `provision` command the cert/key will be saved in a directory named after the thing-type and common name as `deviceCertPlusCACert.crt` and `deviceKey.key`


```bash
$ wintergreen verify --help
Usage: wintergreen verify [OPTIONS]

Options:
  -p, --platform [aws|local]  Platform to upload root CA  [required]
  -t, --thing-type TEXT       AWS IoT thing type  [required]
  -cn, --common_name TEXT     Path to private key  [required]
  --help                      Show this message and exit.

Outputs (depending on success):
Certificate verified on the aws platform! (exit code 0)
Unable to verify certificate on the aws platform... (exit code 1)
```


## Get info about your wintergreen-provisioned devices

```bash
$ wintergreen info --help
Usage: wintergreen info [OPTIONS]

Options:
  -t, --thing-type TEXT    Thing type to receive info about
  -cn, --common_name TEXT  Common name to receive info about
  --help                   Show this message and exit.
```

Check the thing types you have created:

```bash
$ wintergreen info
total thing types: 3
foo
baz
bar
```

Check the things you have provisioned for a given thing type:

```bash
$ wintergreen info -t foo
encryption algorithm: rsa
total things: 3
a33bd27d-6511-4962-8aae-ad2b569b5904
9742c666-e6c0-4410-8ff3-edfe2d1da37b
d43c2e98-4559-45e3-bae5-271406936fbb
```

Get info about a specific thing you have provisioned:


```bash
$ wintergreen info -t foo -cn a33bd27d-6511-4962-8aae-ad2b569b5904
{"date": "2019-12-11", "common_name": "a33bd27d-6511-4962-8aae-ad2b569b5904", "country": "US", "fqdn": "", "locality": "", "organization": "", "state": "", "unit": ""}
```

## The Full Workflow

```bash
$ wintergreen init -t example-thing
{
    "platform_response": {
        "thingTypeName": "example-thing",
        "thingTypeArn": "arn:aws:iot:us-east-1:...",
        "thingTypeId": "...",
        "jitpRoleArn": "arn:aws:iam::...",
        "certificateArn": "arn:aws:iot:us-east-1:..."
    },
    "success": true,
    "platform": "aws"
}

$ wintergreen provision -t example-thing -v
some-uuid-common-name

$ wintergreen verify -t example-thing -cn some-uuid-common-name
Certificate verified on the aws platform!

$ wintergreen info
total thing types: 1
example-thing
```

## Developing Wintergreen

To contribute to the project, please follow the [contributor instructions](CONTRIBUTING.md).
