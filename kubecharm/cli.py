from clint import resources
from path import path
from subparse import CLI
import logging
import yaml


def make_context(cli, args):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return dict(resources=resources.user,
                logger=logger)


def yaml_load(fp):
    with open(fp) as stream:
        return yaml.safe_load(stream)


def genopts(parser):
    fn = 'config.yaml'
    resources.init('kubecharm', 'kfc')
    rpath = path(resources.user.path) / fn
    if not rpath.exists():
        resources.user.write('---\njenkins: {}\n')

    parser.add_argument(
        'config',
        help='A config file to use for kfc',
        default=yaml_load(rpath),
        type=yaml_load)


cli = CLI(version='0.0', context_factory=make_context)
cli.add_generic_options(genopts)
main = cli.run


@cli.command('jujukube.ci:jenkins_job')
def jenkins_job(parser):
    """
    Trigger a charm test build on the remote jenkins slave
    """
    default_jenkins_utils = "http://juju-ci.vapour.ws:8080/job/charm-bundle-test-wip/buildWithParameters"

    parser.add_argument('-j',
                        '--jenkins-api', action='store',
                        help="URL for jenkins api endpoint",
                        type=path,
                        default=default_jenkins_utils)

    parser.add_argument(
        'url',
        help='The charm url to test, typically in the form cs:precise/pictor-1. '
             'Any bundletester-compatible url will work.')
    parser.add_argument(
        '--envs', '-e',
        help='The substrates on which to test',
        default='lxc,aws,hp,azure,joyent',
    )
    parser.add_argument(
        '--callback', '-c',
        help='Callback URL',
        default='',
    )
    parser.add_argument(
        '--job', '-j',
        help='Job ID. Set in jenkins env as JOB_ID.',
        default='',
    )
