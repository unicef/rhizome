import gulp from 'gulp'
import path from 'path'

const jsDestFolder = `${gulp.config('base.dist')}/static/js`
const basedir = path.join(process.cwd(), gulp.config('base.src'))

export default {
  files: [
    {
      'dest': jsDestFolder,
      'options': {
        'basename': 'vendor',
        'basedir': basedir,
        'debug': true
      }
    },
    {
      'entry': `${gulp.config('base.src')}/index.js`,
      'dest': jsDestFolder,
      'options': {
        'debug': true,
        'basename': 'main'
      }
    }
  ],
  options: {
    extensions: ['.jsx', '.js'],
    'transform': [
      'html-browserify',
      'babelify',
      'envify'
    ],
    paths: [
      gulp.config('base.src')
    ],
    plugin: (process.env.NODE_ENV === 'production') ? require('bundle-collapser/plugin') : null
  }
}
