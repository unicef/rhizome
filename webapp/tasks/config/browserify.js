import gulp from 'gulp'
import path from 'path'
import _ from 'lodash'

const vendorBrowser = require(path.join(process.cwd(), gulp.config('base.src'), 'package.json')).browser
const jsDestFolder = `${gulp.config('base.dist')}/static/js`
const basedir = path.join(process.cwd(), gulp.config('base.src'))

export default {
  files: [
    {
      'dest': jsDestFolder,
      'options': {
        'basename': 'vendor',
        'basedir': basedir,
        'debug': true,
        'require': _.map(_.keys(vendorBrowser), function (key) {
          return [
            vendorBrowser[key], {
              expose: key
            }
          ]
        })
      }
    },
    {
      'entry': `${gulp.config('base.src')}/index.js`,
      'dest': jsDestFolder,
      'options': {
        'debug': true,
        'basename': 'main',
        'external': _.keys(vendorBrowser)
      }
    }
  ],
  options: {
    extensions: ['.jsx', '.js'],
    paths: [
      gulp.config('base.src')
    ],
    plugin: (process.env.NODE_ENV === 'production') ? require('bundle-collapser/plugin') : null
  }
}
