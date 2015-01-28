'use strict';
// generated on 2014-10-10 using generator-gulp-webapp 0.1.0

var source     = require('vinyl-source-stream');
var browserify = require('browserify');
var gulp       = require('gulp');
var del        = require('del');
var exec       = require('child_process').exec;

// load plugins
var $ = require('gulp-load-plugins')();

var path = {
	main      : './ui/js/PolioScape.js',
	components: './ui/js/**/*.{js,html,css,sass,scss}',
	js        : './ui/js/**/*.js',
	sass      : ['./ui/styles/**/{screen,print,ie}.scss', './ui/js/**/*.{sass,scss}', './bower_components/**/*.min.css'],
	images    : './ui/img/**/*',
	test      : './ui/test/**/*.js',
	output    : './static',
	clean     : ['./dist', './static', 'build'],
	dist      : 'dist',
	zipfile   : 'uf04-frontend.zip'
};

var build = function (src, dst, opts) {
	var bundleStream = browserify(src, opts).bundle()
		.on('error', function (e) {
			$.util.log(e.message);
			this.emit('end');
		});

	return bundleStream
		.pipe(source(src))
		.pipe($.rename('main.js'))
		.pipe(gulp.dest(dst));
};

gulp.task('styles', function () {
	var filter = $.filter(['**/*', '!ie.css', '!print.css', '!font-awesome.min.css']);

	return gulp.src(path.sass)
		.pipe($.rubySass({
			compass: true,
			style: 'expanded',
			precision: 10
		}))
		.on('error', function (e) {
			$.util.log(e.message);
			this.emit('end');
		})
		.pipe($.flatten())
		.pipe(filter)
		.pipe($.concat('screen.css'))
		.pipe(filter.restore())
		.pipe($.autoprefixer('last 1 version'))
		.pipe(gulp.dest(path.output + '/css'));
});

gulp.task('scripts', function () {
	return gulp.src(path.js)
		.pipe($.jshint())
		.pipe($.jshint.reporter(require('jshint-stylish')));
});

gulp.task('browserify', ['scripts'], function () {
	return build(path.main, path.output, {
		debug: true,
		standalone: 'Polio',
		paths: ['./ui/js']
	});
});

gulp.task('fonts', function () {
	var fonts = $.filter('**/*.{eot,svg,ttf,woff}');

	return $.bowerFiles()
		.pipe($.filter(['**/*.{eot,svg,ttf,woff}']))
		.pipe($.flatten())
		.pipe(gulp.dest(path.output + '/fonts'))
		.pipe($.size());
});

gulp.task('clean', function (cb) {
	del(path.clean, cb);
});

gulp.task('build', ['fonts', 'browserify', 'styles']);
gulp.task('default', ['clean', 'build']);

gulp.task('livereload', function () {
	var server = $.livereload();

	// watch for changes

	gulp.watch(path.output + '/**/*').on('change', function (file) {
		server.changed(file.path);
	});
});

gulp.task('watch', ['browserify', 'styles', 'livereload'], function () {
	gulp.watch('**/*.{scss,sass}', ['styles']);
	gulp.watch(path.components, ['browserify']);
});

gulp.task('test', ['scripts'], function () {
	return gulp.src(path.test).pipe($.mocha());
});

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
			'**/*.{py,sql,html}',
			'requirements.txt',
			'!sql_backups/**/*',
			'!db.sql',
			'!{node_modules,bower_components}/**/*',
			'!**/prod_settings.py'
		])
		.pipe($.zip('uf04-backend.zip'))
		.pipe($.size({ title: 'Backend'}))
		.pipe(gulp.dest(path.dist))
});

gulp.task('dist-ui', ['collectstatic'], function () {
	var jsFilter  = $.filter('**/main.js');
	var cssFilter = $.filter('**/{print,screen,ie}.css');

	return gulp.src('build/**/*')
		.pipe(jsFilter)
		.pipe($.uglify())
		.pipe($.size({ title: 'JavaScript' }))
		.pipe(jsFilter.restore())
		.pipe(cssFilter)
		.pipe($.csso())
		.pipe($.size({ title: 'CSS' }))
		.pipe(cssFilter.restore())
		.pipe($.zip(path.zipfile))
		.pipe($.filter('*.zip'))
		.pipe($.size({ title: 'Zip' }))
		.pipe(gulp.dest(path.dist));
});

gulp.task('dist', ['dist-py', 'dist-ui']);
