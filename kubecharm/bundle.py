"""
The bundle maker and bundle runner logic are contained in this module.
"""
import os
from path import path
import yaml
from . import ci


class Base():
    """
    This class contains the logic to read in the matrix yaml file.
    """
    def __init__(self, matrix):
        """
        Read in the matrix file for the base class.
        """
        with open(matrix, 'r') as stream:
            self.config = yaml.safe_load(stream)


class Maker(Base):
    """
    Contains the logic to generate the bundles which reference different
    versions of kubernetes.
    """

    def __init__(self, matrix, template):
        """
        The Maker class requires a template file to base the bundle on.
        """
        Base.__init__(self, matrix)
        self.template = template

    def configure_bundle(self, template, prefix, release):
        """
        Configure the bundle template for the specific prefix and release.
        """
        # Get a reference to the charms in the template.
        master = template['kubernetes']['services']['kubernetes-master']
        minion = template['kubernetes']['services']['kubernetes']
        etcd = template['kubernetes']['services']['etcd']
        flannel = template['kubernetes']['services']['flannel']

        # Set the version configuration value on the kubernetes-master charm.
        #master['options']['version'] = release
        master['options'] = {'version': release}
        # Set the version configuration value on the kubernetes charm.
        #minion['options']['version'] = release
        minion['options'] = {'version': release}

        if 'head' == prefix:
            # To get Juju to reference github branches change charm and branch:
            # charm: charm-name-0
            # branch: http://github.com/<user>/<charm-project>.git
            master['charm'] = 'kubernetes-master-0'
            master['branch'] = self.config['charms']['kubernetes-master']['github']
            minion['charm'] = 'kubernetes-0'
            minion['branch'] = self.config['charms']['kubernetes']['github']
            etcd['charm'] = 'etcd-0'
            etcd['branch'] = self.config['charms']['etcd']['github']
            flannel['charm'] = 'flannel-0'
            flannel['branch'] = self.config['charms']['flannel']['github']
        else:
            # Launchpad definitions only need the charm definition changed.
            master['charm'] = self.config['charms']['kubernetes-master']['launchpad']
            minion['charm'] = self.config['charms']['kubernetes']['launchpad']
            etcd['charm'] = self.config['charms']['etcd']['launchpad']
            flannel['charm'] = self.config['charms']['flannel']['launchpad']
        return template

    @classmethod
    def generate_bundles_cli(cls, ctx, args):
        """
        Sort out the arguments and the context and generate the bundles.
        """
        matrix = args.matrix
        template = args.template
        generator = cls(matrix, template)
        generator.generate_bundles(args.output)

    def generate_bundles(self, output_directory='specs'):
        """
        Generate the bundles based on the template and configuration
        """
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
        # Generate a bundle for each release.
        for release in self.config['kubernetes-releases']:
            label = self.config['kubernetes-releases'][release]['label']
            for prefix in self.config['bundle_prefixes']:
                template = self.read_template()
                bundle_name = '{0}-{1}-{2}.yaml'.format(prefix, label, release)
                bundle = self.configure_bundle(template, prefix, release)
                bundle_path = os.path.join(output_directory, bundle_name)
                print(bundle_path)
                self.write_bundle(bundle_path, bundle)

    def read_template(self):
        """
        Read the template file to load a bundle structure.
        """
        template = None
        # Read in the bundle template yaml file.
        with open(self.template, 'r') as stream:
            template = yaml.safe_load(stream)
        return template

    def write_bundle(self, file_name, contents):
        """
        Write the bundle structure out to a yaml file.
        """
        with open(file_name, 'w') as stream:
            stream.write(yaml.dump(contents, default_flow_style=False))

# The variable to indicate the class and method to call for the subcommand.
generate = Maker.generate_bundles_cli


class TestRunner(Base):
    """
    Contains the logic to generate the calls to all the bundles based on the
    matrix file.
    """
    @classmethod
    def run_tests_cli(cls, ctx, args):
        matrix = args.matrix
        # Create a TestRunner instance.
        runner = cls(matrix)
        # Get the token from the arguments.
        token = ci.handle_token(args.config, path(ctx['resources'].path))
        runner.run_tests(token)
        return 0

    def run_tests(self, token):
        """
        Run the tests for all bundles as computed by the matrix yaml file.
        """
        api = 'http://juju-ci.vapour.ws:8080/job/charm-bundle-test-wip/buildWithParameters'
        # Specify the environments (docker does not work on LXC).
        env = self.config['environments']
        repository = self.config['bundle_repository']
        # Generate a call to a bundle of each release.
        for release in self.config['kubernetes-releases']:
            label = self.config['kubernetes-releases'][release]['label']
            # Generate one bundle for each prefix.
            for prefix in self.config['bundle_prefixes']:
                # The versioned bundles are stored in the specs directory.
                bundle_name = 'specs/{0}-{1}-{2}.yaml'.format(prefix, label,
                                                              release)
                message = 'Running job on {0} for {1} with bundle {2}'
                print(message.format(env, repository, bundle_name))
                r = ci.run_job(token, repository, env, '', '', bundle_name, api)
                print(r.text)


# The variable to indicate the class and method to call for the subcommand.
test_all_bundles = TestRunner.run_tests_cli
