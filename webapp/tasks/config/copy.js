import gulp from 'gulp'

export default {
  files: [
    {
      src: [
        `${gulp.config('base.src')}/index.html`,
        `assets/**`
      ],
      dest: `${gulp.config('base.dist')}`
    },
    {
      src: [
        'bower_components/fontawesome/fonts/**'
      ],
      dest: `${gulp.config('base.dist')}/fonts`
    }
  ]
}