# awsbuilder


Tools to create and manage AWS resources

## Install

`pip install awsbuilder`

## Configuration

This module must to be run in conjunction with the following configuration files:

* AWS Account configuration [example](example_config/config.yml)
* Environment definition [example](example_config/example_instance_data.yaml)
* EC2 Bootstrap (userdata) script [example](example_config/example_userdata.sh)

## Example Usage

```
awsbuilder -m create -c ~/config.yml -a dev -d ~/instance_data.yml -s search -p courtfinder -e development
```

## Help

```
bash$ awsbuilder --help
  Usage: awsbuilder [options]

  Options:
    -h, --help            show this help message and exit
    -m MODE, --mode=MODE  Mode, server options: [create, delete]
    -c CONFIG, --config=CONFIG
                          Account config path (AWS)
    -d DATA, --data=DATA  Server instance data path
    -s SERVER, --server=SERVER
                          Create a new server
    -a ACCOUNT, --account=ACCOUNT
                          Which AWS account to use from the config file
    -p PROJECT, --project=PROJECT
                          Which project from the instance data file
    -e ENV, --env=ENV     Which environment from the instance data file
```


