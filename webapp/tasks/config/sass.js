import gulp from 'gulp'

const cssDir = `${gulp.config('base.dist')}/css`

export default {
  files: [{
    entry: [
      `${gulp.config('base.src')}/**/style.scss`,
      `styles/screen.scss`
    ],
    src: [
      `${gulp.config('base.src')}/**/style.scss`,
      `styles/*.{,scss,sass}`
    ],
    dest: cssDir,
    options: {
      filename: 'screen.css'
    }
  }, {
    entry: 'styles/print.scss',
    src: [
      `styles/_settings.scss`,
      `styles/print.scss`
    ],
    dest: cssDir
  }],
  options: {
    includePaths: [
      'node_modules/foundation-sites/scss',
      'node_modules/font-awesome/scss',
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