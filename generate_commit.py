import json

with open('version.json') as f:
    versions = json.load(f)
    message = ' • '.join([f'{game} v{version}' for game, version in versions.items()])
    print(message)