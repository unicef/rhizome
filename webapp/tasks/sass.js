import _ from 'lodash'
import gulp from 'gulp'
import gutil from 'gulp-util'
import gulpSass from 'gulp-sass'
import gulpConcat from 'gulp-concat'
import autoprefixer from 'gulp-autoprefixer'

const TASK_NAME = 'sass'

function sassOnce (fileConf) {
  return gulp.src(fileConf.entry)
    .pipe(gulpSass(fileConf.options))
    .on('error', gulpSass.logError)
    .on('error', () => {
      process.exit(1)
    })
    .pipe(_.isArray(fileConf.entry) ? gulpConcat(fileConf.options.filename) : gutil.noop())
    .pipe(autoprefixer(fileConf.options.autoprefixer))
    .pipe(gulp.dest(fileConf.dest))
    .pipe(gulp.pipeTimer(TASK_NAME))
}

function sass () {
  return gulp.autoRegister(TASK_NAME, sassOnce, config => {
    gulp.watch(config.src, evt => {
      gutil.log(evt.type, evt.path)
      sassOnce(config)
    })
  })
}

export default gulp.task(TASK_NAME, sass)
