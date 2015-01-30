#!/usr/bin/env python

import argparse
import requests

JENKINS_URL = 'http://juju-ci.vapour.ws:8080/job/charm-bundle-test-wip/buildWithParameters'
JENKINS_TOKEN = 'wat'


def main():
    parser = argparse.ArgumentParser(
        description="Trigger a charm test build on the remote jenkins slave "
                    "at " + JENKINS_URL,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
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
    args = parser.parse_args()

    params = {
        'token': JENKINS_TOKEN,
        'url': args.url,
        'envs': args.envs,
        'callback_url': args.callback,
        'job_id': args.job,
    }
    response = requests.get(JENKINS_URL, params=params)
    print(response.url)


if __name__ == '__main__':
    main()
