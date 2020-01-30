import json
import os
import shutil
from urllib import request
from zipfile import ZipFile

from pkg_resources import parse_version


def versions(pkg_name):
    url = f'https://pypi.python.org/pypi/{pkg_name}/json'
    response = json.loads(request.urlopen(url).read())
    print(json.dumps(response))
    releases = response['releases']
    latest_versions = sorted(releases, key=parse_version, reverse=True)[0]
    for x in releases[latest_versions]:
        print(x["url"])
        file_name = x["url"]
        new_file_name = "new/{}".format(file_name.split("/")[-1])
        if new_file_name.endswith(".tar.gz"):
            continue
        request.urlretrieve(file_name, new_file_name)

        z = ZipFile(new_file_name)
        x_list = [y for y in z.namelist() if y.endswith(".pyd") or y.endswith(".so")]
        print(x_list)

        if not x_list:
            continue

        with z.open(x_list[0]) as myfile:
            # print(myfile.read())
            with open("bin/{}".format(str(x_list[0]).split("/")[-1]), "bw") as f:
                f.write(myfile.read())

    return True


def build_wheel():
    print(os.listdir(os.path.abspath("bin")))
    dist_path = [x for x in os.listdir(os.path.abspath("dist")) if x.endswith(".whl")][0]
    with ZipFile("dist/{}".format(dist_path), mode='a') as bz:
        for x in tuple(os.listdir(os.path.abspath("bin"))):
            bz.write("bin/{}".format(x), arcname="psycopg2/{}".format(x))

    return True


if __name__ == '__main__':
    if not os.path.exists('new'):
        os.makedirs('new')
    if not os.path.exists('bin'):
        os.makedirs('bin')

    versions("psycopg2-binary")
    # versions("psycopg2")
    build_wheel()
    shutil.rmtree("new")
