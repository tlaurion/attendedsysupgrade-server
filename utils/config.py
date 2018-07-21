import yaml
import os.path
import os
from os import listdir, makedirs
from shutil import copyfile

class Config():
    def __init__(self):
        self.config = {}
        self.config_file = "config.yml"

        if not os.path.exists(self.config_file):
            copyfile(("utils/config.yml.default"), self.config_file)

        with open(self.config_file, 'r') as ymlfile:
            self.config = yaml.load(ymlfile)

        for distro in self.get_distros():
            with open(os.path.join(self.get_folder("distro_folder"), distro, "distro_config.yml"), 'r') as ymlfile:
                self.config[distro] = yaml.load(ymlfile)

            if self.config.get(distro).get("releases"):
                self.config[distro]["latest"] = self.config.get(distro).get("releases")[-1]
            else:
                self.config[distro]["latest"] = None

    def release(self, distro, release):
        release_config = {}
        base_path = self.get_folder("distro_folder") + "/" + distro

        with open(base_path + "/distro_config.yml", 'r') as distro_file:
            release_config.update(yaml.load(distro_file.read()))


        release_path = os.path.join(base_path, distro, release + ".yml")
        if os.path.exists(release_path):
            with open(release_path, 'r') as release_file:
                release_content = yaml.load(release_file.read())
                if release_content:
                    release_config.update(release_content)

        return release_config

    def get(self, opt, alt=None):
        if opt in self.config:
            return self.config[opt]
        return alt

    def get_folder(self, requested_folder):
        folder = self.config.get(requested_folder)
        if folder:
            if not os.path.exists(folder): os.makedirs(folder)
            return os.path.abspath(folder)

        # if unset use $PWD/<requested_folder>
        default_folder = os.path.join(os.getcwdb(), requested_folder)
        if not os.path.exists(default_folder): makedirs(default_folder)
        return os.path.abspath(default_folder)

    def get_distros(self):
        return(listdir(self.config.get("distro_folder")))
