'use strict';
var _ = require('lodash');
var webpackDevConfig = require('./webpack.config.js');
var webpackExamplesConfig = require('./webpack.config.examples.js');

module.exports = function(grunt) {
    // Load grunt tasks automatically
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        // clean out old files from build folders
        clean: {
            build: {
                files: [{
                    dot: true,
                    src: [
                        'build/*', '!build/.git*',
                        'lib/*', '!lib/.git*'
                    ]
                }]
            }
        },

        // transpile JSX/ES6 to normal JS
        // (this is the standard build in lib)
        babel: {
            build: {
                files: [{
                    expand: true,
                    cwd: 'src',
                    src: ['**/*.js', '**/*.jsx'],
                    dest: 'lib',
                    ext: '.js'
                }]
            }
        },

        // also create a self-contained bundle version
        webpack: {
            build: {
                entry: './lib/index.js',
                output: {
                    path: 'build/',
                    filename: 'react-datascope.js'
                }
            },
            examples: webpackExamplesConfig
        },

        // minify bundle
        uglify: {
            build: {
                files: {'build/react-datascope.min.js': 'build/react-datascope.js'}
            }
        },

        watch: {
            build: {
                files: 'src/**/*.*',
                tasks: ['build', 'shell:sayBuiltJs']
            }
        },

        shell: {
            sayBuiltJs: { command: 'say "built js" -v Cellos' }
        },

        'webpack-dev-server': {
            dev: {
                hot: true,
                port: 5709,
                webpack: webpackExamplesConfig,
                publicPath: webpackExamplesConfig.output.publicPath,
                contentBase: 'examples/',
                historyApiFallback: true,
                keepalive: true
            }
        }

    });


    grunt.registerTask('dev', ['build', 'watch']);

    grunt.registerTask('serve', function(target) {
        return grunt.task.run(['webpack-dev-server']);
    });

    grunt.registerTask('examples', function(target) {
        return grunt.task.run(['webpack-dev-server']);
    });

    //grunt.registerTask('build', ['clean', 'babel', 'webpack:build', 'uglify']);
    grunt.registerTask('build', ['clean', 'babel']);
};
