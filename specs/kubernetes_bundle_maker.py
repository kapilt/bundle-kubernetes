#!/usr/bin/env python

# This file kicks off the tests for all versions of Kubernetes.

import os
import subprocess
import yaml

class BundleMaker():
    """
    This class contains the logic to generate the bundles that reference
    different releases of kubernetes, and submit jobs to test those bundles
    on the CI system.
    """

    def __init__(self, configuration_file, template_file):
        """
        Read in the configuration file for the class.
        """
        with open(configuration_file, 'r') as stream:
            self.config = yaml.safe_load(stream)
        with open(template_file, 'r') as stream:
            self.template = yaml.safe_load(stream)

    def configure_bundle(self, template, prefix, release):
        """
        Configure the bundle template for the specific prefix and release.
        """
        master = template['kubernetes']['services']['kubernetes-master']
        master['options']['version'] = release
        minion = template['kubernetes']['services']['kubernetes']
        minion['options']['version'] = release
        etcd = template['kubernetes']['services']['etcd']
        flannel = template['kubernetes']['services']['flannel']
        if 'head' == prefix:
            master['charm'] = 'kubernetes-master-0'
            master['branch'] = self.config['charms']['kubernetes-master']['github']
            minion['charm'] = 'kubernetes-0'
            minion['branch'] = self.config['charms']['kubernetes']['github']
            etcd['charm'] = 'etcd-0'
            etcd['branch'] = self.config['charms']['etcd']['github']
            flannel['charm'] = 'flannel-0'
            flannel['branch'] = self.config['charms']['flannel']['github']
        else:
            master['charm'] = self.config['charms']['kubernetes-master']['launchpad']
            minion['charm'] = self.config['charms']['kubernetes']['launchpad']
            etcd['charm'] = self.config['charms']['etcd']['launchpad']
            flannel['charm'] = self.config['charms']['flannel']['launchpad']
        return template

    def generate_bundles(self, output_directory='specs'):
        """
        Generate the bundles based on the template and configuration
        """
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
        # Generate a bundle for each release.
        for release in self.config['kubernetes-releases']:
            for prefix in self.config['bundle_prefixes']:
                bundle_name = '{0}-{1}.yaml'.format(prefix, release)
                bundle = self.configure_bundle(self.template, prefix, release)
                bundle_path = os.path.join(output_directory, bundle_name)
                print(bundle_path)
                self.write_bundle(bundle_path, bundle)

    def run_tests(self):
        """
        Run the bundle tests for all bundles.
        """
        kfc_command = 'kfc jenkins-job --envs "{0}" -b {1} {2}'
        # Generate a call to a bunlde of each release.
        for release in config['kubernetes-releases']:
            # Specify the environments (docker does not work on LXC).
            env = config['environments']
            repository = config['bundle_repository']
            # Generate one bundle for each prefix.
            for prefix in config['bundle_prefixes']:
                bundle_name = 'specs/{0}-{1}.yaml'.format(prefix, release)
                command = kfc_command.format(env, bundle_name, repository)
                print(command)
                subprocess.check_call(command.split())

    def write_bundle(self, file_name, contents):
        """
        """
        with open(file_name, 'w') as stream:
            stream.write(yaml.dump(contents, default_flow_style=False))

if __name__ == "__main__":
    bundlemaker = BundleMaker('matrix.yaml', '../bundles.yaml')
    bundlemaker.generate_bundles()
