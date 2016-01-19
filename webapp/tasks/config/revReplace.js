import gulp from 'gulp'

const jsDestFolder = `${gulp.config('base.dist')}/static`

export default {
  files: [
    {
      'proManifest': jsDestFolder + '/rev-manifest.json',
      'devManifest': './rev-manifest.json',
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
