import gulp from 'gulp'

const jsDestFolder = `${gulp.config('base.dist')}/static`

export default {
  files: [
    {
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
