import gulp from 'gulp'
import path from 'path'

export default {
  src: [
    '{bin,polio,datapoints,source_data,templates}/**/*.*',
    'webapp*/public*/**/*.*',
    'manage.py',
    'requirements.txt'
  ].map((file)=> {
      return path.join(process.cwd(), '..') + '/' + file;
    }),
  dest: path.join(process.cwd(), '../dist'),
  options: {
    filename: 'rhizome.zip'
  }
}


