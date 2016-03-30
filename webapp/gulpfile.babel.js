import gulp from 'gulp'
import requireDir from 'require-dir'
import gulpTaskConfig from './tasks/libs/gulp-task-config'

gulpTaskConfig(gulp)

requireDir('./tasks')

gulp.config('base.root', '..')
gulp.config('base.src', './src')
gulp.config('base.dist', './public')
gulp.config('templates', '../templates')

gulp.config('tasks', requireDir('./tasks/config'))

gulp.config('tasks.build', {
  taskQueue: [
    'clean',
    'copy',
    'sass',
    'browserify',
    'revCompile',
    'revReplace'
    // 'standard',
  ]
})

gulp.task('dev', () => {
  gulp.config(gulp.DEV_MODE, true)
  gulp.start(['build'])
})

gulp.task('default', ['build'])
