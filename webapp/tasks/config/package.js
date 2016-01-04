import path from 'path'

export default {
  src: [
    '{bin,rhizome,datapoints,source_data,templates,env_var}/**/*.*',
    'webapp*/public*/**/*.*',
    'docs*/_build/**/*.*',
    'manage.py',
    'requirements.txt',
    'settings.py'
  ].map(file => {
    return path.join(process.cwd(), '..') + '/' + file
  }),
  dest: path.join(process.cwd(), '../dist'),
  options: {
    filename: 'rhizome.zip'
  }
}
