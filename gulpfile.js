'use strict';
// generated on 2014-10-10 using generator-gulp-webapp 0.1.0

var source = require('vinyl-source-stream');
var browserify = require('browserify');
var gulp = require('gulp');
var del = require('del');

// load plugins
var $ = require('gulp-load-plugins')();

var path = {
	main: './ui/js/PolioScape.js',
	components: './ui/js/**/*.{js,html,css,sass,scss}',
	js: './ui/js/**/*.js',
	sass: ['./ui/styles/**/{screen,print,ie}.scss', './ui/js/**/*.{sass,scss}', '!./ui/js/bower_components/**/*'],
	images: './ui/img/**/*',
	test: './ui/test/**/*.js',
	output: './static',
	clean: ['./static/**/*.{js,css,html}', '!./static/bower_components/**/*']
};

var build = function (src, dst, opts) {
	var bundleStream = browserify(src, opts).bundle();

	return bundleStream
		.pipe(source(src))
		.pipe($.rename('main.js'))
		.pipe(gulp.dest(dst));
};

gulp.task('styles', function () {
	var filter = $.filter(['**/*', '!ie.css', '!print.css']);

	return gulp.src(path.sass)
		.pipe($.rubySass({
			compass: true,
			style: 'expanded',
			precision: 10
		}))
		.pipe(filter)
		.pipe($.concat('screen.css'))
		.pipe(filter.restore())
		.pipe($.autoprefixer('last 1 version'))
		.pipe(gulp.dest(path.output));
});

gulp.task('scripts', function () {
	return gulp.src(path.js)
		.pipe($.jshint())
		.pipe($.jshint.reporter(require('jshint-stylish')));
});

gulp.task('browserify', ['scripts'], function () {
	return build(path.main, path.output, {
		debug: true,
		standalone: 'Polio'
	});
});

gulp.task('fonts', function () {
	return $.bowerFiles()
		.pipe($.filter('**/*.{eot,svg,ttf,woff}'))
		.pipe($.flatten())
		.pipe(gulp.dest(path.output + '/fonts'))
		.pipe($.size());
});

gulp.task('clean', function (cb) {
	del(path.clean, cb);
});

gulp.task('default', ['clean', 'browserify', 'styles']);

gulp.task('watch', ['browserify', 'styles'], function () {
	var server = $.livereload();

	// watch for changes

	gulp.watch(path.output + '/**/*').on('change', function (file) {
		server.changed(file.path);
	});

	gulp.watch('**/*.{scss,sass}', ['styles']);
	gulp.watch(path.components, ['browserify']);
	gulp.watch(path.images, ['images']);
});

gulp.task('test', ['scripts'], function () {
	return gulp.src(path.test).pipe($.mocha());
});
