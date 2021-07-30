######################
# BXEngine           #
# resourcemanager.py #
# Copyright 2021     #
# Michael D. Reiley  #
######################

# **********
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# **********

import json
import traceback
import sys

import pygame

from lib.logger import init, timestamp, Logger
from lib.util import resource_path


class ResourceManager(object):
    def __init__(self):
        self.resources = {}
        self.config = None
        self.logger = None

    def __contains__(self, item):
        if item in self.resources:
            return True
        return False

    def __getitem__(self, item):
        if self.__contains__(item):
            return self.resources[item]
        else:
            return None

    #def load_schema(self):
    #    pass

    def load_initial_config(self, filename):
        if self.config:
            return self.config
        try:
            with open(filename) as f:
                rsrc = json.load(f)
                # jsonschema.validate(self.config, schema["defaults"])
                self.resources["filename"] = rsrc
                self.config = rsrc
                init(self.config)
                self.logger = Logger("resource")
                return self.config
        except (OSError, IOError):
            print("{0} [config#critical] Could not open bxengine config file: {1}".format(
                timestamp(), filename))
            print(traceback.format_exc(1))
            sys.exit(2)
        except json.JSONDecodeError:
            print("{0} [config#critical] JSON error from bxengine config file: {1}".format(
                timestamp(), filename))
            print(traceback.format_exc(1))
            sys.exit(2)
        #except jsonschema.ValidationError:
        #    print("{0} [config#critical] JSON schema validation error from bxengine config file: {1}".format(
        #        timestamp(), filename))
        #    print(traceback.format_exc(1))
        #    sys.exit(2)

    def load_json(self, filename):
        if filename in self.resources:
            return self.resources[filename]
        try:
            with open(filename) as f:
                rsrc = json.load(f)
                # jsonschema.validate(self.config, schema["defaults"])
                self.resources["filename"] = rsrc
                return self.resources["filename"]
        except (OSError, IOError):
            self.logger.error("Could not open JSON file: {0}".format(filename))
            print(traceback.format_exc(1))
            return None
        except json.JSONDecodeError:
            self.logger.error("JSON error from bxengine config file: {0}".format(filename))
            print(traceback.format_exc(1))
            return None
        #except jsonschema.ValidationError:
        #    self.logger.error("JSON schema validation error from defaults config file: {0}".format(filename))
        #    print(traceback.format_exc(1))
        #    return None

    def load_image(self, filename, scale=None):
        if filename in self.resources:
            return self.resources[filename]
        try:
            if scale:
                rsrc = pygame.transform.scale(pygame.image.load(resource_path(filename)), scale)
            else:
                rsrc = pygame.image.load(resource_path(filename))
            self.resources[filename] = rsrc
            return self.resources[filename]
        except:
            self.logger.error("Could not load image file: {0}".format(filename))