import subprocess
import sys
import codecs


class Configuration(object):
    def __init__(self, wkhtmltopdf='', wkhtmltoimage=''):
        self.wkhtmltopdf = wkhtmltopdf
        self.wkhtmltoimage = wkhtmltoimage
        self.xvfb = 'xvfb-run '

        if not self.wkhtmltopdf:
            if sys.platform == 'win32':
                self.wkhtmltopdf = subprocess.Popen(
                    ['where', 'wkhtmltopdf'], stdout=subprocess.PIPE).communicate()[0].strip()
            elif 'linux' in sys.platform:
                self.wkhtmltopdf = self.xvfb + subprocess.Popen(
                    ['which', 'wkhtmltopdf'], stdout=subprocess.PIPE).communicate()[0].strip()
            else:
                self.wkhtmltopdf = subprocess.Popen(
                    ['which', 'wkhtmltopdf'], stdout=subprocess.PIPE).communicate()[0].strip()

        if not self.wkhtmltoimage:
            if sys.platform == 'win32':
                self.wkhtmltoimage = subprocess.Popen(
                    ['where', 'wkhtmltoimage'], stdout=subprocess.PIPE).communicate()[0].strip()
            elif 'linux' in sys.platform:
                self.wkhtmltoimage = self.xvfb + subprocess.Popen(
                    ['which', 'wkhtmltoimage'], stdout=subprocess.PIPE).communicate()[0].strip()
            else:
                self.wkhtmltoimage = subprocess.Popen(
                    ['which', 'wkhtmltoimage'], stdout=subprocess.PIPE).communicate()[0].strip()



def print_pdf(type, url, output_path, options=None, cookie=None, css_file=None):
    configuration = Configuration()

    if 'pdf' in type:
        wk_command = configuration.wkhtmltopdf.decode('utf-8')
    else:
        wk_command = configuration.wkhtmltoimage.decode('utf-8')

    command = [wk_command]
    if options:
        for key, value in list(options.items()):
            if not '--' in key:
                normalized_key = '--%s' % str(key)
            else:
                normalized_key = str(key)
            command += [normalized_key, value]
    if cookie:
        command += ['--cookie', cookie['name'], cookie['value']]
    if css_file:
        command += ['--user-style-sheet', css_file]
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

    if 'cannot connect to X server' in stderr.decode('utf-8'):
        return IOError('%s\n'
                    'You will need to run whktmltopdf within a "virutal" X server.\n'
                    'Go to the link above for more information\n'
                    'https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server' % stderr.decode('utf-8'))

    if 'Error' in stderr.decode('utf-8'):
        return IOError('wkhtmltopdf reported an error:\n' + stderr.decode('utf-8'))

    if exit_code != 0:
        return IOError("wkhtmltopdf exited with non-zero code {0}. error:\n{1}".format(exit_code, stderr.decode("utf-8")))

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
                    return IOError('Command failed: %s\n'
                                  'Check whhtmltopdf output without \'quiet\' '
                                  'option' % ' '.join(args))
                return True
        except IOError:
            return IOError('Command failed: %s\n'
                          'Check whhtmltopdf output without \'quiet\' option' %
                          ' '.join(args))
