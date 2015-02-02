from clint.textui import prompt
from path import path
import requests
import yaml


def handle_token(config, configfp):
    token = config['jenkins'].get('token', None)
    if token is None:
        token = prompt.query('You must enter a Jenkins token:')
        if token is None:
            raise RuntimeError("You must have a token.")

        store = prompt.yn('Would you like to store your token?')
        if store is True:
            config['jenkins']['token'] = token
            cf = configfp / "config.yaml"
            with open(cf, 'w') as stream:
                yaml.safe_dump(config, stream)
    return token


def jenkins_job(ctx, args, handle_token=handle_token):
    token = handle_token(args.config, path(ctx['resources'].path))
    params = {
        'token': token,
        'url': args.url,
        'envs': args.envs,
        'callback_url': args.callback,
        'job_id': args.job,
        'bundle': args.bundle
    }
    response = requests.get(args.jenkins_api, params=params)
    print(response.url)
