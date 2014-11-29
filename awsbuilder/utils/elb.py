import sys
import boto.ec2.elb


class ELB:

    conn_elb = None
    config = None
    endpoint = None
    valid_config = None

    def __init__(self, config):
        self.config = config
        if self.config.aws_access is not None and self.config.aws_secret is not None:
            self.conn_elb = boto.ec2.elb.connect_to_region(
                region_name=self.config.region,
                aws_access_key_id=self.config.aws_access,
                aws_secret_access_key=self.config.aws_secret)
            try:
                self.config.config['elb']
                self.valid_config = True
            except KeyError:
                self.valid_config = False
        else:
            print "[ERROR] No AWS credentials"
            sys.exit(1)

    def create(self):
        if self.valid_config:
            conf = self.config.config['elb']
            listeners = []
            for i in conf['listeners']:
                listeners.append(conf['listeners'][i])

            lb = self.conn_elb.create_load_balancer(conf['name'],
                                               ['eu-west-1a', 'eu-west-1b'],
                                               listeners=listeners,
                                               security_groups=conf['security_groups'].keys())

            lb.enable_cross_zone_load_balancing()
            print
            print "ELB Built", lb.dns_name
            print

    def get_lb_by_name(self, name):
        try:
            return self.conn_elb.get_all_load_balancers([name])[0]
        except:
            return None

    def add_instances(self, name, instances):
        self.get_lb_by_name(name).register_instances(instances)
        print "Added to LB [%s]:" % name, instances

    def delete(self):
        if self.valid_config:
            if self.config.env != 'live' and self.get_lb_by_name(self.config.config['elb']['name']) is not None:
                self.conn_elb.delete_load_balancer(self.config.config['elb']['name'])
                print "\nDeleting ELB:", self.config.config['elb']['name']
            else:
                print "\nNo ELB to delete:", self.config.config['elb']['name']

