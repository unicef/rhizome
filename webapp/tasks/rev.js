import gulp from 'gulp'
import _ from 'lodash'

import fs from 'fs'
import browserify from 'browserify'
import watchify from 'watchify'
import rev from 'gulp-rev'
import rename from 'gulp-rename'
import handlebars from 'gulp-compile-handlebars'

const TASK_NAME = 'rev'

function gulpRev (config) {
  return gulp.src([config.entry + '/**/*.css', config.entry + '/**/*.js'])
      .pipe(gulp.dest(config.dest))
      .pipe(rev())
      .pipe(gulp.dest(config.dest))
      .pipe(rev.manifest())
      .pipe(gulp.dest('./'))
}

function revCompile (config) {
  var manifest = JSON.parse(fs.readFileSync(config.revManifest, 'utf8'))

  var handlebarOpts = {
    helpers: {
      assetPath: function (path, context) { return [context.data.root[path]].join('/') }
    }
  }

  return gulp.src(config.templates + '/base.hbs')
        .pipe(handlebars(manifest, handlebarOpts))
        .pipe(rename('base.html'))
        .pipe(gulp.dest(config.templates))
}

function revOnce (config = {}) {
  gulpRev(config)
  return revCompile(config)
}

function revTask () {
  return gulp.autoRegister(TASK_NAME, revOnce, config => {
    config.bundler = browserify(_.merge({}, config.options))
    config.bundler = watchify(config.bundler)

    config.bundler.on('update', gulpRev.bind(null, config))
    config.bundler.on('update', revCompile.bind(null, config))
  })
}

gulp.task(TASK_NAME, revTask)

export default revTask
