import gulp from 'gulp'

export default {
  src: [
    `styles/**/*.{,scss,sass}`
  ],
  dest: `${gulp.config('base.dist')}/css`,
  options: {
    includePaths: [
      'bower_components',
      'node_modules/jeet/scss/jeet'
    ],
    autoprefixer: {
      browsers: [
        'ie >= 8',
        'ie_mob >= 10',
        'ff >= 30',
        'chrome >= 34',
        'safari >= 7',
        'opera >= 23',
        'ios >= 7',
        'android >= 2.3',
        'bb >= 10'
      ]
    }
  }
}