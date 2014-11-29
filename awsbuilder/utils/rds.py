import sys
import time
import boto.rds


class RDS:

    conn_rds = None
    config = None
    endpoint = None
    valid_config = None

    def __init__(self, config):
        self.config = config
        if self.config.aws_access is not None and self.config.aws_secret is not None:
            self.conn_rds = boto.rds.connect_to_region(
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
            conf = self.config.config['rds']
            try:
                self.conn_rds.create_dbinstance(
                    id=conf['id'],
                    db_name=conf['db_name'],
                    allocated_storage=conf['allocated_storage'],
                    instance_class=conf['instance_class'],
                    master_username=conf['master_username'],
                    master_password=conf['master_password'],
                    port=conf['port'],
                    engine=conf['engine'],
                    engine_version=conf['engine_version'],
                    auto_minor_version_upgrade=conf['auto_minor_version_upgrade'],
                    multi_az=conf['multi_az'],
                    backup_retention_period=conf['backup_retention_period'])
                print "RDS Built"
            except Exception, e:
                print '[ERROR]:', e

    def get_db_instance(self, db_id):
        for db in self.conn_rds.get_all_dbinstances():
            if db.id == db_id:
                return db

    def get_db_status(self, db_id):
        db = self.get_db_instance(db_id)
        if str(db.status) == "available":
            return True
        else:
            return False

    def delete(self):
        if self.valid_config:
            db = self.get_db_instance(self.config.config['rds']['id'])
            if self.config.env != 'live' and db is not None:
                if db.status == "available":
                    self.conn_rds.delete_dbinstance(db.id, skip_final_snapshot=True)
                    print "Deleting RDS:", self.config.config['rds']['id']
                else:
                    print "\nRDS being deleted:", self.config.config['rds']['id']
            else:
                print "\nNo RDS to delete:", self.config.config['rds']['id']
