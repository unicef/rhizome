import gulp from 'gulp'
import del from 'del'

const TASK_NAME = 'clean'

function clean(callback) {
  gulp.autoRegister(TASK_NAME, (config)=> {
    del.sync(config.src)
    callback()
  })
}

gulp.task(TASK_NAME, clean)

export default clean

