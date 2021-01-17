# -*- coding: utf-8 -*-
# (c) 2016-2020 Andreas Motl <andreas@getkotori.org>
import os
import re
import sys
import logging
import uuid
from io import StringIO

import arrow
from bunch import Bunch
from appdirs import user_cache_dir
from tempfile import NamedTemporaryFile
from contextlib import contextmanager
from pprint import pformat
from cornice.util import to_list
from git import Repo
from git import RemoteProgress
from plumbum import local
from plumbum.cmd import pwd, make, grep, ls
from kotori.util.errors import last_error_and_traceback

log = logging.getLogger(__name__)

# http://gitpython.readthedocs.io/en/stable/tutorial.html
# https://shell.readthedocs.io/en/latest/tutorial.html

"""
Todo
====

Prio 1
------
- [x] Return stderr and Python traceback in case of error
- [x] Finalize http pathway, incl. success (Content-Disposition) and failure (text/plain)
- [x] Run from system cache dir
- [x] Running "make" and "make firmware-info" consecutively takes too much time!
      Refactor into make target which has "all" as dependency target
- [x] Put "BOARD_TAG" and "BOARD_SUB" values from Makefile into "self.build_result"
      or maybe just pull them into the transformation dict, also with build path (target_path)
- [x] Don't forget to re-enable "origin.fetch" and "self.repo.submodule_update"

Prio 2
------
- [o] Option "prune" for pruning the buildpath before building
- [o] Option "clean" for running "make clean" before building
- [o] Add more logging to different "acquire_source" steps
- [o] Option for running "avr-strip" before handing out the ELF file
- [o] Add timing information to "self.build_result"
- [o] Propagate some information from "self.build_result" to HTTP response headers
- [o] Also redirect logging output to "self.stream"

Prio 3
------
- [o] Make configurable from which directory to run from to improve concurrent building (e.g. using a token)
- [o] Option "ansi=false" for disabling "CXXFLAGS += -fdiagnostics-color" in Makefile
- [o] Option for packaging the whole source tree in its state when building the software into a source tarball,
  including output from "git diff"
- [o] Make more generic by injecting Makefile
- [o] Make even more generic by making it handle arbitrary regular repositories of Arduino code
- [o] Bind gitlab/github webhook to "prune" operation
"""

class ProgressPrinter(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):

        if not message:
            return

        parts = (op_code, cur_count, max_count, cur_count / (max_count or 100.0), message or u"NO MESSAGE")
        parts = list(map(str, parts))
        message = u' '.join(parts)
        padding = u' ' * 120

        # STDERR
        #sys.stderr.write(message.strip() + padding)
        #sys.stderr.write('\r')
        #sys.stderr.write('\n')

        # Logger
        log.info(message)

class FirmwareBuilder(object):

    def __init__(self, repo_url=None, repo_branch='master', update_submodules=True, workingdir='.', architecture=None, esp_root=None):
        self.repo = None
        self.repo_url = repo_url
        self.repo_branch = repo_branch
        self.update_submodules = update_submodules
        self.workingdir = workingdir
        self.architecture = architecture or 'avr'
        self.esp_root = esp_root
        self.stream = sys.stderr

        self.repo_info = {}
        self.build_result = {}

        self.variable_patterns = [

            # Preprocessor defines .ino, .pde, .cpp, .h, e.g.
            # #define HE_USER         "testdrive"
            '#define\s+(?P<name>{name})\s+(?P<value>.+)',

            # Makefile variables, e.g.
            # BOARD_TAG         = pro328
            '^(?!#)(?P<name>{name})\s+:?=\s+(?P<value>.*)$',
            ]

    def acquire_source(self):

        cache_dir = os.path.join(user_cache_dir('kotori'), 'firmware-builder', 'sources')
        if not os.path.isdir(cache_dir): os.makedirs(cache_dir)

        target_path = os.path.join(cache_dir, os.path.basename(self.repo_url))

        log.info('Build path is {target_path}'.format(target_path=target_path))

        # 1. Get hold of repository
        if os.path.isdir(target_path):

            # Define repository object from existing path
            # http://gitpython.readthedocs.io/en/stable/tutorial.html#meet-the-repo-type
            self.repo = Repo(target_path)

            # Fetch updates from remote
            # http://gitpython.readthedocs.io/en/stable/tutorial.html#handling-remotes
            origin = self.repo.remotes.origin
            log.info('Fetching updates from repository {repository}'.format(repository=origin.url))
            origin.fetch(progress=ProgressPrinter())

        else:

            # Clone repository from a remote
            log.info('Cloning repository {repository}'.format(repository=self.repo_url))
            self.repo = Repo.clone_from(self.repo_url, target_path, progress=ProgressPrinter())


        # Default effective gitref to given reference label (either branch/tag name or commit sha)
        gitref_effective = self.repo_branch

        # Compute effective gitref by searching the origin branches for the given reference label
        origin = self.repo.remotes.origin
        origin_branch_ref = origin.name + '/' + self.repo_branch
        for ref in origin.refs:
            if ref.name == origin_branch_ref:
                gitref_effective = ref.name


        # 2. Switch to designated branch/gitref
        # http://gitpython.readthedocs.io/en/stable/tutorial.html#switching-branches

        # Point the HEAD symbolic reference to the designated gitref
        self.repo.head.reference = gitref_effective

        # Brutally reset the index and working tree to match the pointed-to commit
        # Attention: Don't do this on a real repository you are working on, data may get lost!
        self.repo.head.reset(index=True, working_tree=True)


        # 3. Initialize submodules
        # http://gitpython.readthedocs.io/en/stable/tutorial.html#advanced-repo-usage
        # update all submodules, non-recursively to save time, this method is very powerful, go have a look
        if self.update_submodules:
            log.info('Updating git submodules')
            self.repo.submodule_update(recursive=True, progress=ProgressPrinter())
        else:
            log.info('Skip updating git submodules')

        # Return some information about repository
        self.repo_info = {
            'remote': origin.url,
            'ref': gitref_effective,
            'commit': self.repo.head.commit.hexsha[:8],
        }

    def patch_files(self, filepatterns, data):

        filepatterns = to_list(filepatterns)

        directory = os.path.join(self.repo.working_dir, self.workingdir)

        # cd into appropriate directory
        with local.cwd(directory):
            for pattern in filepatterns:

                # Find files matching pattern in directory
                # This is plumbum's syntax for shell globbing
                path = local.path()
                lp_files = path // str(pattern)

                # Iterate and patch all files
                for lp_file in lp_files:
                    filepath = str(lp_file)
                    self.patch_file(filepath, data)

    def patch_file(self, filepath, data):

        log.info('Patching file {filepath}'.format(**locals()))

        # Read file
        payload = open(filepath, 'r').read()

        # Machinery for computing replacements
        replacements = []
        for name, value in data.items():
            for match in self.find_variable(payload, name, multiline=True):

                value_before = match['value']

                is_quoted = value_before.startswith('"')

                # Debugging: Provoke build error when replacing e.g. GPRSBEE_AP_NAME
                #is_quoted = value_before.startswith('"') and value_before.endswith('"')

                replacement = str(value)
                if is_quoted:
                    replacement = '"' + replacement + '"'
                match['line-after'] = match['line-before'].replace(value_before, replacement)
                replacements.append(match)

        log.info('Replacements:\n%s', pformat(replacements))

        # Apply replacements
        for replacement in replacements:
            payload = payload.replace(replacement['line-before'], replacement['line-after'])

        # Write file
        open(filepath, 'w').write(payload)

    def find_variable(self, payload, name, multiline=False):
        for pattern_template in self.variable_patterns:
            pattern = pattern_template.format(name=name)
            if multiline:
                matcher = re.compile(pattern, re.MULTILINE)
            else:
                matcher = re.compile(pattern)
            for m in matcher.finditer(payload):
                match = m.groupdict()
                match['line-before'] = m.group(0)
                # Exit inner loop
                break
            else:
                # Cycle outer loop when having no matches
                continue

            yield match

    def run_build(self, makefile=None):
        log.info('Running build')
        if self.architecture.lower() == 'esp':
            with local.env(ESP_ROOT=self.esp_root):
                return self.run_makefile(makefile=makefile)
        else:
            return self.run_makefile(makefile=makefile)

    def run_makefile(self, makefile=None):
        """
        Run the whole build process with designated Makefile.
        """

        # cd into git repository directory
        with local.cwd(self.repo.working_dir):

            # cd into working directory inside git repository
            with local.cwd(self.workingdir):

                # Run Makefile to start the compilation process
                make('--file', makefile, 'all-plus-firmware-info', stdout=self.stream, stderr=self.stream)

                # Slurp output of build process
                try:
                    self.stream.seek(0)
                    output = self.stream.read()
                except IOError:
                    make_firmware_info = make['--file', makefile, 'firmware-info'] | grep['TARGET_']
                    output = make_firmware_info()

                # Grep "TARGET_HEX", "TARGET_ELF" (for AVR) as well as "TARGET_BIN" and "TARGET_CHIP" (for ESP) paths
                # from build output and store into "self.build_result"
                target_matcher = re.compile('(?P<name>TARGET_.+):(?: (?P<value>.+))?')
                for m in target_matcher.finditer(output):
                    match = m.groupdict()
                    name  = match['name']
                    value = match['value']
                    if value:
                        self.build_result[name] = value

                # Add build path to build result
                self.build_result['build_path'] = pwd().strip()

    def make_artefact(self):
        artefact = Artefact()

        artefact.architecture = self.architecture
        artefact.source = self.repo_info
        artefact.build  = self.build_result

        # AVR
        if self.architecture == 'avr':
            target_hex = os.path.abspath(os.path.join(self.build_result['build_path'], self.build_result['TARGET_HEX']))
            target_elf = os.path.abspath(os.path.join(self.build_result['build_path'], self.build_result['TARGET_ELF']))

            artefact.name = os.path.splitext(os.path.basename(target_hex))[0]
            artefact.binary.hex = open(target_hex, 'rb').read()
            artefact.binary.elf = open(target_elf, 'rb').read()

        # ESP
        elif self.architecture == 'esp':
            target_bin = os.path.abspath(self.build_result['TARGET_BIN'])
            artefact.name = os.path.splitext(os.path.basename(target_bin))[0]
            artefact.binary.bin = open(target_bin, 'rb').read()

        return artefact

    @contextmanager
    def capture(self):
        """
        Capture output of the whole build process.
        Return stacktrace of Python driver and output of make command, if any.
        """

        # The result object containing build success flag and error outputs.
        # This gets bound to the context manager variable.
        result = Bunch()
        self.build_result['capture'] = result

        # A temporary file to redirect make output to
        self.stream = NamedTemporaryFile()
        try:
            # Pass execution flow to context manager body,
            # effectively running the main build process
            yield result

            # Signal success if build engine completed
            result.success = True

        except Exception as ex:

            # Signal failure
            result.success = False

            # Capture Python traceback
            result.error = last_error_and_traceback()

        # Capture make output
        self.stream.seek(0)
        result.output = self.stream.read()

    def error_message(self):

        result = self.build_result['capture']
        buf = StringIO()
        width = 80

        print(u'=' * width, file=buf)
        print(u'INFO'.center(width), file=buf)
        print(u'=' * width, file=buf)
        print(file=buf)
        print('Repository:', file=buf)
        print(pformat(self.repo_info, indent=12), file=buf)
        print(file=buf)
        print('Directory: ', self.workingdir, file=buf)
        print(file=buf)

        print(u'=' * width, file=buf)
        print(u'ERROR'.center(width), file=buf)
        print(u'=' * width, file=buf)
        print(file=buf)
        print(result.error.decode('utf-8'), file=buf)
        print(file=buf)

        print(u'=' * width, file=buf)
        print(u'OUTPUT'.center(width), file=buf)
        print(u'=' * width, file=buf)
        print(file=buf)
        print(result.output.decode('utf-8'), file=buf)

        return buf.getvalue()

class Artefact(object):

    def __init__(self):

        # TODO: Add more build arguments
        # TODO: Persist somehow
        # TODO: Display contents on html page

        self.architecture = None
        self.source  = None
        self.build   = None
        self.name    = None

        self.binary  = BinaryArtefact()

        self.identifier = str(uuid.uuid4())
        self.timestamp  = arrow.now().format('YYYYMMDDTHHmmss')

    def get_binary(self, suffix):
        return getattr(self.binary, suffix)

    @property
    def commit_sha(self):
        return self.source['commit']

    @property
    def fullname(self):

        template = '{name}_{architecture}-{target}_{timestamp}_{commit}_{identifier}'

        target = 'unknown'
        commit = self.commit_sha

        if self.architecture == 'avr':
            target = '{board_tag}-{board_sub}'.format(
                board_tag = self.build.get('TARGET_BOARD_TAG', 'unknown'),
                board_sub = self.build.get('TARGET_BOARD_SUB', 'unknown')
            )

        elif self.architecture == 'esp':
            target = '{target_chip}'.format(
                target_chip = self.build.get('TARGET_CHIP', 'unknown'),
            )

        variables = {}
        variables.update(**self.__dict__)
        variables.update(**locals())

        result = template.format(**variables)

        return result

    def __repr__(self):
        hex_size = self.binary.hex and len(self.binary.hex) or None
        elf_size = self.binary.elf and len(self.binary.elf) or None
        bin_size = self.binary.bin and len(self.binary.bin) or None
        tplvars = {}
        tplvars.update(**self.__dict__)
        tplvars.update(**locals())
        return u'<{class_} name={name} source={source} hexsize={hex_size} elfsize={elf_size} binsize={bin_size}>'.format(class_=type(self).__name__, **tplvars)


class BinaryArtefact:

    def __init__(self):

        self.hex     = None
        self.elf     = None
        self.bin     = None



# ------------------------------------------
#   Example program
# ------------------------------------------

def example_recipe(fb):

    fb.acquire_source()

    data = {
        'BOARD_TAG': 'mega2560',
        'BOARD_SUB': 'atmega2560',
        'HE_USER': 'Hotzenplotz',
        'HE_SITE': 'Buxtehude',
        'HE_HIVE': 'Raeuberhoehle',
        'GPRSBEE_APN': 'internet.altes-land.de',
        'GPRSBEE_APNUSER': 'kaschperl',
        'GPRSBEE_APNPASS': '12345',
        'GPRSBEE_VCC': 23,
        }
    fb.patch_files(['*.ino', '*.pde', '*.cpp', '*.h', 'Makefile*'], data)

    fb.run_makefile(makefile='Makefile-OSX.mk')
    #fb.run_makefile(makefile='Makefile-FWB.mk')
    artefact = fb.make_artefact()
    #print artefact.elf

    return artefact

def firmware_builder():
    repo_url = 'https://github.com/hiveeyes/arduino'
    return FirmwareBuilder(repo_url=repo_url, repo_branch='master', workingdir='node-gprs-any')

def run_example():
    fb = firmware_builder()
    artefact = example_recipe(fb)
    log.info(u'Build succeeded, artefact: {}'.format(artefact))

def capture_example():
    fb = firmware_builder()
    with fb.capture() as result:
        artefact = example_recipe(fb)

    print(list(fb.build_result.keys()))

    if result.success:
        log.info(u'Build succeeded, artefact: {}'.format(artefact))
    else:
        log.error(u'Build failed\n{message}'.format(message=fb.error_message()))

    return result


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    #run_example()
    result = capture_example()
    print(result.output)

