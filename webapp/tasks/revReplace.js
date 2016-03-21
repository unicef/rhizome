import gulp from 'gulp'
import _ from 'lodash'

import fs from 'fs'
import browserify from 'browserify'
import watchify from 'watchify'
import rename from 'gulp-rename'
import handlebars from 'gulp-compile-handlebars'

const TASK_NAME = 'revReplace'

function revCompile (config) {
  var manifestFile = JSON.parse(fs.readFileSync(config.manifestFile, 'utf8'))

  var handlebarOpts = {
    helpers: {
      assetPath: function (path, context) { return [context.data.root[path]].join('/') }
    }
  }

  return gulp.src(config.templates + '/base.hbs')
        .pipe(handlebars(manifestFile, handlebarOpts))
        .pipe(rename('base.html'))
        .pipe(gulp.dest(config.templates))
}

function revOnce (config = {}) {
  return revCompile(config)
}

function revTask () {
  return gulp.autoRegister(TASK_NAME, revOnce, config => {
    config.bundler = browserify(_.merge({}, config.options))
    config.bundler = watchify(config.bundler)

    config.bundler.on('update', revCompile.bind(null, config))
  })
}

gulp.task(TASK_NAME, revTask)

export default revTask
