import json
import os
from urllib import request
from zipfile import ZipFile

from pkg_resources import parse_version

BIN_PATH = "bin"


def is_valid_file(file_name: str):
    valid = file_name.endswith(".pyd")
    valid = valid or file_name.endswith(".so")
    valid = valid or ("psycopg2_binary.libs/" in file_name and len(file_name.strip("/").split("/")) > 1)
    valid = valid or ".dylibs/" in file_name
    return valid


def versions(pkg_name):
    url = f'https://pypi.python.org/pypi/{pkg_name}/json'
    response = json.loads(request.urlopen(url).read())
    # print(json.dumps(response))
    releases = response['releases']
    latest_versions = sorted(releases, key=parse_version, reverse=True)[0]
    for x in releases[latest_versions]:
        # print(x["url"])
        file_name = x["url"]
        new_file_name = "new/{}".format(file_name.split("/")[-1])
        if new_file_name.endswith(".tar.gz"):
            continue
        if not (
                "2_17" in new_file_name or "2_24" in new_file_name or "win" in new_file_name or "macosx" in new_file_name
        ):
            continue
        request.urlretrieve(file_name, new_file_name)
        print(new_file_name)
        z = ZipFile(new_file_name)
        x_list = [
            y for y in z.namelist() if is_valid_file(y)
        ]
        # print(x_list)

        for x_file in x_list:
            with z.open(x_file) as myfile:
                with open("{}/{}".format(BIN_PATH, str(x_file).replace("psycopg2/", "")), "bw") as f:
                    f.write(myfile.read())

    return True


def build_wheel():
    # print(os.listdir(os.path.abspath(BIN_PATH)))
    dist_path = [x for x in os.listdir(os.path.abspath("dist")) if x.endswith(".whl")][0]
    with ZipFile("dist/{}".format(dist_path), mode='a') as bz:
        for x in [os.path.join(path, name) for path, subdirs, files in os.walk(BIN_PATH) for name in files]:
            original_file = x.lstrip(BIN_PATH).lstrip('\\').lstrip("/")
            if "psycopg2_binary.libs" in x:
                bz.write(x, arcname="{}".format(original_file))
            else:
                bz.write(x, arcname="psycopg2/{}".format(original_file))

    return True


if __name__ == '__main__':
    if not os.path.exists('new'):
        os.makedirs('new')
    if not os.path.exists(BIN_PATH):
        os.makedirs(BIN_PATH)

    if not os.path.exists("{}/{}".format(BIN_PATH, ".dylibs")):
        os.makedirs("{}/{}".format(BIN_PATH, ".dylibs"))

    if not os.path.exists("{}/{}".format(BIN_PATH, "psycopg2_binary.libs")):
        os.makedirs("{}/{}".format(BIN_PATH, "psycopg2_binary.libs"))

    versions("psycopg2-binary")
    # versions("psycopg2")
    build_wheel()
    # shutil.rmtree("new")
