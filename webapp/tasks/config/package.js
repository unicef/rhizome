import path from 'path'

export default {
  src: [
    '{bin,rhizome,datapoints,templates,env_var}/**/*.*',
    'webapp*/public*/**/*.*',
    'docs*/_build/**/*.*',
    'manage.py',
    'appspec.yml',
    'requirements.txt',
    'settings.py',
    '*.xlsx',
    '*.csv'
  ].map(file => {
    return path.join(process.cwd(), '..') + '/' + file
  }),
  dest: path.join(process.cwd(), '../dist'),
  options: {
    filename: 'rhizome.zip'
  }
}
