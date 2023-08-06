# coding=utf-8
import os
import subprocess


def build_image(client, path, tag, dockerfile, no_build, no_cache=False):
    if not no_build:
        cmd = ["docker", "build", "--pull", "-t", tag, "-f", dockerfile]
        if no_cache:
            cmd.append("--no-cache")
        with open(dockerfile) as _:
            contents = _.read()
        vname = 'AIDO_REGISTRY'
        if vname in contents:
            value = os.environ.get(vname)
            cmd.append(['--build-arg', f'{vname}={value}'])
        cmd.append(path)
        subprocess.check_call(cmd)

    image = client.images.get(tag)
    return image
