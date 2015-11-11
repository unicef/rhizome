import gulp from 'gulp'

export default {
  files: [
    {
      src: [
        `${gulp.config('base.src')}/index.html`
      ],
      dest: `${gulp.config('base.dist')}`
    },
    {
      src: [
        `${gulp.config('base.src')}/assets/**/*.*`
      ],
      dest: `${gulp.config('base.dist')}/static`
    },
    {
      src: [
        'node_modules/font-awesome/fonts/**'
      ],
      dest: `${gulp.config('base.dist')}/static/fonts`
    }
  ]
}
