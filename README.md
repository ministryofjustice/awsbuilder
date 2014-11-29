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
awsbuilder -a <aws_access_key> -s <aws_secret_key> -m create -c config.yml -e dev -i ec2
```

## Help

```
bash$ awsbuilder --help
Usage: awsbuilder [options]

Options:
  -h, --help            show this help message and exit
  -a AWS_ACCESS, --access=AWS_ACCESS
                        AWS Access key
  -s AWS_SECRET, --secret=AWS_SECRET
                        AWS Secret key
  -m MODE, --mode=MODE  Mode [create or delete]
  -e ENV, --env=ENV     Set the environment
  -i ITEM, --item=ITEM  Set the AWS service item you want create/delete
                        [ec2,elb,elasticache,rds]
  -c CONFIG, --config=CONFIG
                        Override the default config.yml file
```


