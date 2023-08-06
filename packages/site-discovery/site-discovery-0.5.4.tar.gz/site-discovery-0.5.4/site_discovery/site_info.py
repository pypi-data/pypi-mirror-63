import argparse
import os
import re
import sys
import signal
import subprocess
from pprint import pprint
import sh
import time
import json
import urllib.request, urllib.parse, urllib.error
import yaml
from influxdb import line_protocol
import datetime

def signal_handler(signal, frame):
    sys.exit(0)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description='site-info')
    parser.add_argument(
        'root_path', help='Path to site root directory', nargs='?', default=os.getcwd())
    parser.add_argument('--format',
                        action='store', dest='output_format', default='console',
                        help='Output format (console, json, line)')
    parser.add_argument('--log-path',
                        action='store', dest='log_path', default='',
                        help='Write to log')
    parser.add_argument('--log-format',
                        action='store', dest='log_format', default='json',
                        help='Log format (console, json, line)')
    parser.add_argument('--group',
                        action='append', dest='groups', default=['main'],
                        help='Groups of site-info tests')
    parser.add_argument('--only',
                        action='store', dest='only', default='',
                        help='Run only tests with names')

    args = parser.parse_args()

    if args.only == '':
        args.only = []
    else:
        args.only = args.only.split(',')

    # table = DrupalsTable(root_paths=root_paths, suites_limit=suites_limit, tests_limit=tests_limit,
    # 	data_xlsx_filename=options.data_xlsx_filename, data_json_filename=options.data_json_filename,
    # 	only_tests=only_tests, only_groups=only_groups, term_output=term_output)

    site_info = SiteInfo(args)
    if not os.path.isdir(site_info.root_path):
        eprint("%s is not directory" % site_info.root_path)
    else:
        site_info.prepare()
        site_info.run()

    site_info.output()


class SiteInfo():
    def __init__(self, args):
        self.groups = args.groups
        self.only = args.only
        self.root_path = args.root_path
        self.output_format = args.output_format
        self.log_path = args.log_path
        self.log_format = args.log_format
        self.tests = []
        self.data = {}
        self.reset()

    def prepare(self):
        self.add_data('engine', self.get_engine())

        self.tests_config = self.get_tests()
        self.tests_config = [x for x in self.tests_config
                                      if not 'engine' in x or x['engine'] == self.data['engine']]
        for test_config in self.tests_config:
            self.add_test(test_config)

    def get_engine(self):
        os.chdir(self.root_path)
        engine = sh.Command('get-engine')
        engine = 'unknown'
        if os.path.exists(self.root_path + '/configuration.php'):
            engine = 'joomla'
        elif os.path.exists(self.root_path + '/wp-login.php'):
            engine = 'wordpress'
        elif os.path.exists(self.root_path + '/bitrix'):
            engine = 'bitrix'
        elif os.path.exists(self.root_path + '/sites/default/settings.php'):
            engine = 'drupal'
        elif not os.path.exists(self.root_path + '/index.php'):
            engine = 'none'
        return engine

    def add_test(self, test_config):
        self.tests.append(SiteTest(test_config))
        return self

    def get_all_tests(self):
        tests_config = {}
        paths = [
            '/etc/site-info.yml',
            os.path.expanduser('~') + '/site-info.yml'
        ]

        for path in paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    tests_config = yaml.load(f, Loader=yaml.FullLoader)

        if not tests_config:
            print("No site-info.yml found, or empty, aborting.")
            sys.exit(1)

        for t in tests_config['tests']:
            # normalize config
            if 'groups' in t:
                if not isinstance(t['groups'], (list)):
                    t['groups'] = [t['groups']]
            else:
                t['groups'] = []

        return tests_config

    def get_tests(self):
        tests_config = self.get_all_tests()
        groups = self.groups
        only = self.only
        filtered = []

        # filter by only
        if len(only) > 0:
            for t in tests_config['tests']:
                if 'name' in t and t['name'] in only:
                    filtered.append(t)
            return filtered

        # no filter
        if 'all' in groups:
            return tests_config['tests']

        # filter by group
        for t in tests_config['tests']:
            # filter by groups intersection
            intersect = list(set(groups) & set(t['groups']))
            if intersect:
                filtered.append(t)
        return filtered

    def reset(self):
        for test in self.tests:
            test.result = None
            test.time = 0
        self._results = []

    def run(self):
        if sys.version_info.major == 2:
            domain = os.path.basename(self.root_path).decode('idna')
        else:
            domain = os.path.basename(self.root_path)

        self.add_data('domain', domain)

        for t in self.tests:
            # some tests has not command, for viasite-projects
            if not t.command:
                continue

            t.command = t.command.replace('${DOMAIN}', self.data['domain'])
            os.chdir(self.root_path)

            t.run()
            if self.output_format == 'console':
                #delta = self.get_delta(self.get_last_result(t.name), t.result)
                delta = 0
                t.out_console(
                    color_output=True,
                    delta=delta
                )

        data = self.get_data()

    def get_output(self, data, format):
        if format == 'console':
            output = ''
            for t in data:
                if t['name'] in['time', 'result', 'result_percent']:
                    #delta = self.get_delta(t['last_result'], t['result'])
                    output += '%s: %s\n' % (t['name'], t['result'])
            output += '\n'
            return output

        elif format == 'json':
            json_raw = json.dumps(data)
            return json_raw

        if format == 'line':
            measurement = 'site_info'
            fields = {}
            tags = {}

            # pprint(data)
            for t in data:
                if t['result'] is None:
                    continue;

                if t['type'] == 'boolean':
                    # both fields and tags
                    val = 1 if t['result'] else 0
                    tags[t['name']] = val
                    fields[t['name']] = val

                elif t['type'] == 'integer' or t['type'] == 'float' or t['type'] == 'time':
                    fields[t['name']] = t['result']

                else:
                    tags[t['name']] = t['result']

            data = {'points': [{
                'measurement': 'site_info',
                'tags': tags,
                'fields': fields,
                'time': datetime.datetime.utcnow()
            }]}

            return line_protocol.make_lines(data)

    def output(self):
        data = self.get_data()

        # write to log
        if self.log_path:
            with open(self.log_path, "a") as log:
                log.write(self.get_output(data, self.log_format))

        print(self.get_output(data, self.output_format))

    def add_data(self, name, value):
        self.data[name] = value

    """
    Get all test data: name, results, validation.
    Generate summary columns.
    Using for generate all other.
    """

    def get_data(self, group=None):
        if self._results and not group:
            return self._results

        row = []

        time = 0
        result = 0
        max_result = 0

        for test in self.tests:
            if group and group not in test.groups:
                continue

            if not test.command:
                continue

            # default type integer
            if not hasattr(test, 'type'):
                test.type = 'integer'

            # types fix
            try:
                if test.result == '':
                    test.result = None
                else:
                    if test.type == 'boolean':
                        if test.result == '0':
                            test.result = False
                        elif test.result == '1':
                            test.result = True
                        else:
                            test.result = None
                    elif test.type == 'integer':
                        test.result = int(float(test.result))
                    elif test.type == 'float':
                        test.result = float(test.result)
                    elif test.type == 'time':
                        test.result = int(float(test.result))
                    #else:
                    #    test.result = str(test.result)
                        # pprint(test.result)
            except:
                test.result = None

            col = {
                'name': test.name,
                'type': test.type,
                'result': test.result,
                #'last_result': self.get_last_result(test.name),
                'valid': test.valid_str(),
                'time': test.time,
                'comment': test.comment,
                'groups': test.groups
            }

            time += test.time
            if test.valid() == 'Warn':
                result += 1
            elif test.valid() == True:
                result += 2
            max_result += test.max_result()

            row.append(col)

        row.append({
            'name': 'time',
            'type': 'time',
            'result': time,
            #'last_result':self.get_last_result('time'),
            'valid': None
        })

        # Summary for all site tests
        row.append({
            'name': 'result',
            'type': 'integer',
            'result': result,
            #'last_result':self.get_last_result('result'),
            'valid': None
        })

        row.append({
            'name': 'max_result',
            'type': 'integer',
            'result': max_result,
            'valid': None
        })

        row.append({
            'name': 'result_percent',
            'type': 'integer',
            'result': int(float(result) / max_result * 100) if max_result > 0 else 0,
            #'last_result':self.get_last_result('result_percent'),
            'valid': None
        })

        self._results = row
        return self._results


"""
SiteTest - single test (one column)
"""


class SiteTest():

    def __init__(self, *initial_data):
        self.validate = {}
        self.command = None

        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])

        # 0 - False, 1 - Warn, 2 - True
        self.result = None
        self.time = 0

        self.comment = self.validate['comment'] if type(self.validate) is dict and 'comment' in self.validate else None

        if not hasattr(self, 'groups'):
            self.groups = []

    """
    Execute test command, get result, output to console
    """

    def run(self):
        started = time.time()
        if self.command is not None:
            proc = subprocess.Popen(
                self.command, stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            self.result = out.strip().decode('utf-8')

            # integer values
            intRegex = re.compile('^[0-9]+$')
            if (not hasattr(self, 'type') or self.type == 'integer') and intRegex.match(self.result):
                self.result = int(self.result)

            self.time = int((time.time() - started) * 1000) # msec
            return self.result

    """
    Color output of result to console
    """

    def out_console(self, color_output=True, delta=None):
        valid = self.valid()
        nc = '\033[0m'

        colors = {
            None: '',
            'pass': '\033[32m',
            'warn': '\033[33m',
            'fail': '\033[31m'
        }

        if not color_output:
            colors['pass'] = colors['warn'] = colors['fail'] = ''
            nc = ''

        color = colors[self.valid_str()]

        # TODO: color_output disables comment output, for cron
        comment = (' (%s)' %
                   self.comment if self.comment and color_output else '')
        delta_text = ''
        if delta:
            delta_color = colors['pass'] if delta > 0 else colors['warn']
            delta_text = ' (%s%s%s%s)' % (
                delta_color, ('+' if delta > 0 else ''), delta, nc)

        print('%s: %s%s%s%s%s' % (self.name, color, self.result, nc, delta_text, comment))

    def validable(self):
        if self.validate is None or not self.validate:
            return False
        return True

    def max_result(self):
        return 2 if self.validable() else 0

    """
    Result check.
    Returns: None|True|False|Warn|result
    """

    def valid(self):
        rules = self.validate
        result = self.result

        if not self.validable() or result is None or result == '':
            return None

        # elif rules=='result':
        #	return result

        valid = self._check(result, rules)
        if valid:
            return True
        elif isinstance(rules, dict) and 'warning' in rules:
            warning = self._check(result, rules['warning'])
            if warning:
                return 'Warn'

        return False

    def valid_str(self):
        return {
            None: None,
            True: 'pass',
            'Warn': 'warn',
            False: 'fail'
        }[self.valid()]

    """
    Result validation
    Return True if matches rule
    If rule is empty then rule matches (TODO: will problems with it)
    """

    def _check(self, result, rules):

        if isinstance(rules, dict):
            if isinstance(result, str) and result.isdigit():
                result = float(result)

            if 'max' in rules and int(result) > int(rules['max']):
                # print('%d > %d' % (result, rules['max']))
                return False

            if 'min' in rules and int(result) < int(rules['min']):
                return False

        else:
            if self.type == 'boolean':
                return bool(result) or int(result) == int(rules)
            return result == rules

        return True


if __name__ == '__main__':
    main()
