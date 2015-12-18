import subprocess
import sys
import codecs


class Configuration(object):
    def __init__(self, wkhtmltopdf=''):
        self.wkhtmltopdf = wkhtmltopdf

        if not self.wkhtmltopdf:
            if sys.platform == 'win32':
                self.wkhtmltopdf = subprocess.Popen(
                    ['where', 'wkhtmltopdf'], stdout=subprocess.PIPE).communicate()[0].strip()
            else:
                self.wkhtmltopdf = subprocess.Popen(
                    ['which', 'wkhtmltopdf'], stdout=subprocess.PIPE).communicate()[0].strip()

        try:
            result = subprocess.Popen(self.wkhtmltopdf, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
            stdout, stderr = result.communicate()
            if 'cannot connect to X server' in stderr.decode('utf-8'):
                self .wkhtmltopdf = 'xvfb-run ' + subprocess.Popen(
                    ['which', 'wkhtmltopdf'], stdout=subprocess.PIPE).communicate()[0].strip()
        except IOError:
            raise IOError('%s\n'
                      'You will need to run whktmltopdf within a "virutal" X server.\n'
                      'Go to the link above for more information\n'
                      'https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server' % stderr.decode('utf-8'))

        try:
            with open(self.wkhtmltopdf) as f:
                pass
        except IOError:
            raise IOError('No wkhtmltopdf executable found: "%s"\n'
                          'If this file exists please check that this process can '
                          'read it. Otherwise please install wkhtmltopdf - '
                          'https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf' % self.wkhtmltopdf)


def print_pdf(url, output_path, options=None, cookie=None):
    configuration = Configuration()
    wkhtmltopdf = configuration.wkhtmltopdf.decode('utf-8')
    command = [wkhtmltopdf]
    if options:
        for key, value in list(options.items()):
            if not '--' in key:
                normalized_key = '--%s' % str(key)
            else:
                normalized_key = str(key)
            command += [normalized_key, value]
    if cookie:
        command += ['--cookie', cookie['name'], cookie['value']]
    if url:
        command += [url]
    if output_path:
        command += [output_path]
    else:
        command += '-'
    command = ' '.join(command)
    return to_pdf(command, output_path)


def to_pdf(args, path=None):
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    stdout, stderr = result.communicate()

    exit_code = result.returncode

    if 'Error' in stderr.decode('utf-8'):
        raise IOError('wkhtmltopdf reported an error:\n' + stderr.decode('utf-8'))

    if exit_code != 0:
        raise IOError("wkhtmltopdf exited with non-zero code {0}. error:\n{1}".format(exit_code, stderr.decode("utf-8")))

    if '--quiet' not in args:
        sys.stdout.write(stderr.decode('utf-8'))

    if not path:
        return stdout
    else:
        try:
            with codecs.open(path, encoding='utf-8') as f:
                # read 4 bytes to get PDF signature '%PDF'
                text = f.read(4)
                if text == '':
                    raise IOError('Command failed: %s\n'
                                  'Check whhtmltopdf output without \'quiet\' '
                                  'option' % ' '.join(args))
                return True
        except IOError:
            raise IOError('Command failed: %s\n'
                          'Check whhtmltopdf output without \'quiet\' option' %
                          ' '.join(args))
