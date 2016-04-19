import gulp from 'gulp'
import zip from 'gulp-zip'

const TASK_NAME = 'package'

function packageTask () {
  gulp.autoRegister(TASK_NAME, config => {
    return gulp.src(config.src)
      .pipe(zip(config.options.filename))
      .pipe(gulp.dest(config.dest))
  })
}

gulp.task(TASK_NAME, packageTask)

export default packageTask
