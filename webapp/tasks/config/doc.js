import gulp from 'gulp'

export default {
  files: [
    {
      src: `${gulp.config('base.root')}/docs/front-end/**/*.md`,
      dist: `${gulp.config('base.root')}/docs/_build/front-end/`
    }
  ]
}
