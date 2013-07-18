import os
import ConfigParser
import logging

logger = logging.getLogger(__name__)


def load_aws_config():
    """
    Loads the AWS_CONFIG_FILE for the specified enviroment
    """
    config_path = os.environ.get('AWS_CONFIG_FILE',
                                 os.path.expanduser('~/.aws/aws_config_file'))

    if not os.path.exists(config_path):
        raise Exception('Not found aws_config_file')

    environment = os.environ.get('AWS_ENVIRONMENT', 'default')
    try:
        config = ConfigParser.ConfigParser()
        config.readfp(open(config_path))
        return dict((x, y) for x, y in reversed(config.items(environment)))
    except ConfigParser.NoSectionError:
        raise Exception('Not found environment %s '
                        'on configuration' % environment)

aws_config = load_aws_config()

AUTH = {'aws_access_key_id': aws_config.get('aws_access_key_id'),
        'aws_secret_access_key': aws_config.get('aws_secret_access_key')}

DEFAULT_REGION = aws_config.get('region')

EC2_LAUNCH_CONFIGS = {
    'ubuntu-12.10_us-east-1': {
        'description': 'Ubuntu 12.10.',
        'ami': 'ami-f6700c9f', #12.10 64, ebs
        'instance_type': 'm1.small',
        'security_groups': ['puppet-test'],
        'region': DEFAULT_REGION,
        'key_name': 'niedbalski',
        'availability_zone': 'a',
        'tags': {
            'awsfab-ssh-user': 'ubuntu'
        },
    }
}
