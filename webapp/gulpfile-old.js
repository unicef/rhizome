gulp.task('collectstatic', ['build'], function (cb) {
  exec('python manage.py collectstatic --noinput -v 0', function (err) {
    if (err) {
      return cb(err);
    }

    cb();
  });
});

gulp.task('dist-py', function () {
  return gulp.src([
    '{bin,polio,datapoints,source_data,entity,templates,static}/**/*.{py,sql,html,sh,css,js}',
    'manage.py',
    'requirements.txt',
    'webpack-stats.json',
  ])
    .pipe($.zip('rhizome.zip'))
    .pipe($.size({title: 'Backend'}))
    .pipe(gulp.dest(path.dist))
});
