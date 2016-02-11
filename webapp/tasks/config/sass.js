import gulp from 'gulp'

const cssDir = `${gulp.config('base.dist')}/static/css`

export default {
  files: [{
    entry: [
      `${gulp.config('base.src')}/**/style.scss`,
      `${gulp.config('base.src')}/assets/styles/screen.scss`
    ],
    src: [
      `${gulp.config('base.src')}/**/style.scss`,
      `${gulp.config('base.src')}/assets/styles/**/*.{,scss,sass}`
    ],
    dest: cssDir,
    options: {
      filename: 'screen.css'
    }
  }, {
    entry: `${gulp.config('base.src')}/assets/styles/pdf.scss`,
    src: [
      `${gulp.config('base.src')}/assets/styles/_settings.scss`,
      `${gulp.config('base.src')}/assets/styles/pdf.scss`
    ],
    dest: cssDir
  }, {
    entry: `${gulp.config('base.src')}/assets/styles/print-redesign.scss`,
    src: [
      `${gulp.config('base.src')}/assets/styles/_settings.scss`,
      `${gulp.config('base.src')}/assets/styles/print-redesign.scss`
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
