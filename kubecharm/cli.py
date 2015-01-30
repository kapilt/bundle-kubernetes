from clint import resources
from path import path
from subparse import CLI
import logging
import yaml


def make_context(cli, args):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return dict(logger=logger)


def genopts(parser):
    resources.init('config.yaml', 'kfc')
    import pdb;pdb.set_trace()
    # parser.add_argument('-p', '--releasepath', action='store',
    #                     help="path to cf-release",
    #                     type=path,
    #                     default=path('.').abspath() / 'cf-release')

    # parser.add_argument('-i', '--index', action='store',
    #                     help="URL of compiled package index",
    #                     default=s3_url(default_bucket))

    # #@@ calculated latest release
    # parser.add_argument('-n',  '--release-number', action='store',
    #                     default='180',
    #                     help="Release number")

cli = CLI(version='0.0', context_factory=make_context)
cli.add_generic_options(genopts)
main = cli.run

@cli.command('jujukube.ci:jenkins_job')
def jenkins_job(parser):
    """
    Kick off a jenkins job for a bundle
    """
    pass
