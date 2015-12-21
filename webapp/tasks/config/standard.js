import gulp from 'gulp'

export default {
  files: [{
    entry: [
      `${gulp.config('base.src')}/**/*.js{,x}`
    ],
    src: [
      `${gulp.config('base.src')}/**/*.js{,x}`
    ]
  }]
}
