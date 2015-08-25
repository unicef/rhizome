import gulp from 'gulp'
import gutil from 'gulp-util'
import gulpSass from 'gulp-sass'
import autoprefixer from 'gulp-autoprefixer'

const TASK_NAME = 'sass'

function sassOnce(fileConf) {
  return gulp.src(fileConf.src)
    .pipe(gulpSass(fileConf.options))
    .on('error', gulpSass.logError)
    .pipe(autoprefixer(fileConf.options.autoprefixer))
    .pipe(gulp.dest(fileConf.dest))
    .pipe(gulp.pipeTimer(TASK_NAME))
}

function sass() {
  return gulp.autoRegister(TASK_NAME, sassOnce, (config)=> {
    gulp.watch(config.src, (evt)=> {
      gutil.log(evt.type, evt.path)
      sassOnce(config)
    })
  })
}

export default gulp.task(TASK_NAME, sass)
