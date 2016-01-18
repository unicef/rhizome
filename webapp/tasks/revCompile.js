import gulp from 'gulp'
import _ from 'lodash'

import browserify from 'browserify'
import watchify from 'watchify'
import rev from 'gulp-rev'

const TASK_NAME = 'revCompile'

function gulpRev (config) {
  return gulp.src([config.entry + '/**/*.css', config.entry + '/**/*.js'])
      .pipe(gulp.dest(config.dest))
      .pipe(rev())
      .pipe(gulp.dest(config.dest))
      .pipe(rev.manifest())
      .pipe(gulp.dest(config.dest))
}

function revOnce (config = {}) {
  return gulpRev(config)
}

function revTask () {
  return gulp.autoRegister(TASK_NAME, revOnce, config => {
    config.bundler = browserify(_.merge({}, config.options))
    config.bundler = watchify(config.bundler)

    config.bundler.on('update', gulpRev.bind(null, config))
  })
}

gulp.task(TASK_NAME, revTask)

export default revTask
