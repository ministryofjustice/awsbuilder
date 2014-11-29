import sys
import time
import boto.iam


class IAM:

    conn_iam = None
    config = None
    endpoint = None

    def __init__(self, config):
        self.config = config
        if self.config.aws_access is not None and self.config.aws_secret is not None:
            self.conn_iam = boto.iam.connect_to_region(
                region_name=self.config.region,
                aws_access_key_id=self.config.aws_access,
                aws_secret_access_key=self.config.aws_secret)
        else:
            print "[ERROR] No AWS credentials"
            sys.exit(1)

    def list(self):
        print self.conn_iam.get_all_server_certs()['list_server_certificates_response']['list_server_certificates_result']['server_certificate_metadata_list']
