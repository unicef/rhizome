import gulp from 'gulp'

const jsDestFolder = `${gulp.config('base.dist')}/static`
var proManifest =  jsDestFolder + '/rev-manifest.json'
var devManifest = './rev-manifest.json'
var manifestFile = (process.env.NODE_ENV === 'production') ? proManifest : devManifest

export default {
  files: [
    {
      'manifestFile': manifestFile,
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
