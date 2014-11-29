import sys
import time
import boto.ec2
from elb import ELB


class EC2:

    conn_ec2 = None
    config = None
    endpoint = None
    valid_config = None

    def __init__(self, config):
        self.config = config
        if self.config.aws_access is not None and self.config.aws_secret is not None:
            self.conn_ec2 = boto.ec2.connect_to_region(
                region_name=self.config.region,
                aws_access_key_id=self.config.aws_access,
                aws_secret_access_key=self.config.aws_secret)
            try:
                self.config.config['ec2']
                self.valid_config = True
            except KeyError:
                self.valid_config = False
        else:
            print "[ERROR] No AWS credentials"
            sys.exit(1)

    def create(self):
        if self.valid_config:
            conf = self.config.config['ec2']
            for i in conf:
                print i
                userdata = None
                try:
                    userdata = conf[i]['userdata']
                except KeyError:
                    pass
                reservation = self.conn_ec2.run_instances(conf[i]['ami'],
                                            key_name=conf[i]['key_name'],
                                            instance_type=conf[i]['instance_type'],
                                            security_groups=conf[i]['security_groups'],
                                            instance_initiated_shutdown_behavior='terminate',
                                            user_data=userdata)

                instance = reservation.instances[0]

                print "Sleeping 5s while EC2 wakes up..."
                time.sleep(5)

                status = instance.update()
                while status != 'running':
                    time.sleep(10)
                    print "Sleeping for 10 more seconds (not ready yet...)"
                    status = instance.update()

                # Set the tags for the instance when 'running'
                if status == 'running':
                    for tag in conf[i]['tags']:
                        instance.add_tag(str(tag), str(conf[i]['tags'][tag]))
                        print "[EC2] Set Instance Tag to %s:%s" % (str(tag), str(conf[i]['tags'][tag]))

                print instance.id
                try:
                    if 'elb' in conf[i]:
                        # TODO - currently cannot deal with multiple ELB's
                        elb = ELB(self.config)
                        elb.add_instances(self.config.config['elb']['name'], [str(instance.id)])
                except:
                    pass

    def get_all_security_groups(self):
        return self.conn_ec2.get_all_security_groups()

    def get_all_instances_by_env(self):
        instances = []
        for s in self.conn_ec2.get_all_instances():
            try:
                if str(s.instances[0].tags['Env']) == self.config.env and str(s.instances[0]._state) == 'running(16)':
                    instances.append(s.instances[0])
            except:
                pass
        return instances

    def delete(self):
        if self.valid_config:
            # GET LIST OF SERVERS FOR AN ENV
            instances = self.get_all_instances_by_env()

            # GET LIST OF SERVER ROLE TAG:Name to verify before deleting
            valid_servers = []
            for i in self.config.config['ec2']:
                valid_servers.append(self.config.config['ec2'][i]['tags']['Name'])

            # CHECK THE ENV IS NOT PROD AND IS A VALID SERVER
            if self.config.env != 'prod' and len(instances) > 0:
                for i in instances:
                    if str(i.tags['Name']) in valid_servers:
                        i.terminate()
                        print "\nDeleting EC2's [%s]: %s" % (self.config.env, i)
            else:
                print "\nNo EC2's to delete:", self.config.env
