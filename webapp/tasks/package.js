import gulp from 'gulp'
import zip from 'gulp-zip'

const TASK_NAME = 'package'

function packageTask () {
  let counter = 1
  gulp.autoRegister(TASK_NAME, config => {
    console.log('Iteration: ', counter)
    console.log('=============================\n')
    console.log('config.src: ', config.src)
    console.log('=============================\n')
    console.log('config.options.filename: ', config.options.filename)
    console.log('=============================\n')
    console.log('config.dest: ', config.dest)
    console.log('=============================')
    return gulp.src(config.src)
      .pipe(zip(config.options.filename))
      .pipe(gulp.dest(config.dest))
  })
}
console.log('Running TASK_NAME:', TASK_NAME)
console.log('\n')
console.log('packageTask', packageTask)
console.log('\n')
console.log('=============================')
gulp.task(TASK_NAME, packageTask)

export default packageTask
