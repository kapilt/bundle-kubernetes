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
        resources.user.write(fn, '---\njenkins: {}\n')

    parser.add_argument(
        '--config',
        help='A config file to use for kfc',
        default=yaml_load(rpath),
        type=yaml_load)


cli = CLI(version='0.0', context_factory=make_context)
cli.add_generic_options(genopts)
main = cli.run


@cli.command('kubecharm.bundle:test_all_bundles')
def test_all_bundles(parser):
    """
    Trigger a bundle test job on for each bundle defined in the
    specs/matrix.yaml file.
    """
    default_matrix = 'specs/matrix.yaml'
    parser.add_argument('-m',
                        '--matrix', action='store',
                        help='The path to the matrix file that contains the'
                        ' permutations of the bundles to test.',
                        type=path,
                        default=default_matrix)


@cli.command('kubecharm.bundle:generate')
def generate_bundles(parser):
    """
    Generate all the combinations of bundles from the matrix file, basing the
    bundle on the template file, storing the output in a directory.
    """
    default_matrix = 'specs/matrix.yaml'
    default_template = 'bundles.yaml'
    default_output = 'specs'
    parser.add_argument('-m',
                        '--matrix',
                        action='store',
                        help='The path to the matrix file that contains the'
                             ' permutations of the bundles to test.',
                        type=path,
                        default=default_matrix)
    parser.add_argument('-t',
                        '--template',
                        action='store',
                        help='The relative path to the bundle to use as the'
                        ' template (the main bundles.yaml works fine).',
                        type=path,
                        default=default_template)
    parser.add_argument('-o',
                        '--output',
                        action='store',
                        help='The relative path to the output directory.',
                        type=path,
                        default=default_output)


@cli.command('kubecharm.ci:jenkins_job')
def jenkins_job(parser):
    """
    Trigger a charm test build on the remote jenkins slave
    """
    default_jenkins_utils = "http://juju-ci.vapour.ws:8080/job/charm-bundle-test-wip/buildWithParameters"

    parser.add_argument('-u',
                        '--jenkins-api', action='store',
                        help="URL for jenkins api endpoint",
                        type=path,
                        default=default_jenkins_utils)

    parser.add_argument('-b',
                        '--bundle', action='store',
                        help="Relative path for a bundle to run",
                        type=path,
                        default='./bundles.yaml')

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
