import gulp from 'gulp'
import runSequence from 'run-sequence'

const TASK_NAME = 'build'

function build (callback) {
  const conf = gulp.config(['tasks', TASK_NAME])
  runSequence.apply(gulp, [].concat(conf.taskQueue).concat(callback))
}

gulp.task(TASK_NAME, build)

export default build
