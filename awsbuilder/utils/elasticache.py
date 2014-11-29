import sys
import time
import boto.elasticache


class Elasticache:

    conn_ec = None
    config = None
    endpoint = None
    valid_config = None

    def __init__(self, config):
        self.config = config
        if self.config.aws_access is not None and self.config.aws_secret is not None:
            self.conn_ec = boto.elasticache.connect_to_region(
                region_name=self.config.region,
                aws_access_key_id=self.config.aws_access,
                aws_secret_access_key=self.config.aws_secret)
            try:
                self.config.config['elasticache']
                self.valid_config = True
            except KeyError:
                self.valid_config = False

        else:
            print "[ERROR] No AWS credentials"
            sys.exit(1)

    def create(self):
        if self.valid_config:
            conf = self.config.config['elasticache']
            self.conn_ec.create_cache_cluster(
                conf['cache_cluster_id'],
                num_cache_nodes=conf['num_cache_nodes'],
                cache_node_type=conf['cache_node_type'],
                engine=conf['engine'],
                engine_version=conf['engine_version'],
                security_group_ids=conf['security_group_ids'])
            print "Elasticache Built"

    def get_cache_endpoint(self, ec_id):
        ec = self.get_ec_instance(ec_id)
        return ec['ConfigurationEndpoint']['Address']

    def get_ec_instance(self, ec_id):
        ec = self.conn_ec.describe_cache_clusters()
        for cache in ec["DescribeCacheClustersResponse"]["DescribeCacheClustersResult"]["CacheClusters"]:
            if str(cache['CacheClusterId']) == ec_id:
                return cache

    def get_ec_status(self, ec_id):
        ec = self.get_ec_instance(ec_id)
        if str(ec['CacheClusterStatus']) == "available":
            return True
        else:
            return False

    def delete(self):
        if self.valid_config:
            cache = self.get_ec_instance(self.config.config['elasticache']['cache_cluster_id'])
            if self.config.env != 'live' and cache is not None:
                if str(cache['CacheClusterStatus']) == 'available':
                    self.conn_ec.delete_cache_cluster(self.config.config['elasticache']['cache_cluster_id'])
                    print "\nDeleting Elasticache:", self.config.config['elasticache']['cache_cluster_id']
                else:
                    print "\nElasticache being deleted:", self.config.config['elasticache']['cache_cluster_id']
            else:
                print "\nNo Elasticache to delete:", self.config.config['elasticache']['cache_cluster_id']
