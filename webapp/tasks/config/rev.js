import gulp from 'gulp'
import path from 'path'
import _ from 'lodash'

const jsDestFolder = `${gulp.config('base.dist')}/static`

export default {
  files: [
    {
      'revManifest': './rev-manifest.json',
      'templates': `${gulp.config('templates')}`,
      'entry': jsDestFolder,
      'dest': jsDestFolder
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
