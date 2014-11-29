import yaml


class Config:

    config = None
    env = None

    def __init__(self, access, secret, region='eu-west-1'):
        self.aws_access = access
        self.aws_secret = secret
        self.region = region

    def set_config_from_file(self, fp, env):
        self.config = yaml.load(open(fp).read())[env]
        self.env = env

