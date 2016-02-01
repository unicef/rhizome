import gulp from 'gulp'

export default {
  files: [{
    entry: [
      `${gulp.config('base.src')}/**/*.js{,x}`,
      `!${gulp.config('base.src')}/util/parsers/**`
    ],
    src: [
      `${gulp.config('base.src')}/**/*.js{,x}`,
      `!${gulp.config('base.src')}/util/parsers/**`
    ]
  }]
}
