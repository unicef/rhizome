import gulp from 'gulp'
// import gutil from 'gulp-util'
// import gulpStandard from 'gulp-standard'

const TASK_NAME = 'standard'

// function standardOnce (fileConf) {
//   return gulp.src(fileConf.src)
//     .pipe(gulpStandard())
//     .pipe(gulpStandard.reporter('default', {
//       breakOnError: true
//     }))
//     .pipe(gulp.pipeTimer(TASK_NAME))
// }

// function standardWatch (targetFile) {
//   return gulp.src(targetFile)
//     .pipe(gulpStandard())
//     .pipe(gulpStandard.reporter('default', {
//       breakOnError: false
//     }))
//     .pipe(gulp.pipeTimer(TASK_NAME))
// }
function standard () {
  console.log('skipping')
  // return gulp.autoRegister(TASK_NAME, standardOnce, config => {
  //   gulp.watch(config.src, evt => {
  //     gutil.log(evt.type, evt.path)
  //     standardWatch(evt.path)
  //   })
  // })
}

export default gulp.task(TASK_NAME, standard)
