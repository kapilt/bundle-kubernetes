#!/usr/bin/env python3

# This file contains the python3 tests for the Kubernetes Juju bundle.

import amulet
import os
import unittest
import yaml

seconds = 1200


class BundleIntegrationTest(unittest.TestCase):
    """ This class creates an integration test for deploying a bundle. """
    bundle = None

    def setUpClass(self):
        """ This method deploys the bundle one level up. """
        if self.bundle:
            self.bundle_path = os.path.abspath(self.bundle)
        else:
            self.bundle_path = os.path.join(os.path.dirname(__file__),
                                            '..',
                                            'bundles.yaml')

        self.deployment = amulet.Deployment()
        try:
            with open(self.bundle_path, 'r') as bundle_file:
                contents = yaml.safe_load(bundle_file)
                self.deployment.load(contents)
            self.deployment.setup(seconds)
            self.deployment.wait()
        except Exception:
            message = 'Unable to set up environment in %d seconds.' % seconds
            amulet.raise_status(amulet.FAIL, msg=message)

    def kunits(self):
        """ Return a tuple of the relevant units. """
        return (self.deployment.sentry.unit['kubernetes/0'],
                self.deployment.sentry.unit['kubernetes/1'],
                self.deployment.sentry.unit['kubernetes-master/0'])

    def test_0_unit_existance(self):
        """ Test the unit existance. """
        assert self.deployment.sentry.unit.get('kubernetes/0', False)
        assert self.deployment.sentry.unit.get('kubernetes/1', False)
        assert self.deployment.sentry.unit.get('kubernetes-master/0', False)

    def test_1_relations(self):
        """ Test bundle relations, errors will be thrown if relations fail. """
        kube0, kube1, km = self.kunits()
        # Get all the important relations from the bundle.
        etcd_relation = kube0.relation('etcd', 'etcd:client')
        master_relation = kube0.relation('api',
                                         'kubernetes-master:minions-api')
        minion_relation = km.relation('minions-api', 'kubernetes:api')
        return etcd_relation, master_relation, minion_relation


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bundle', default=None)
    pargs = parser.parse_args()
    BundleIntegrationTest.bundle = pargs.bundle
    unittest.main()
