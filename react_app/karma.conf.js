var path = require('path')

module.exports = function (config) {
  config.set({
    browsers: ['Chrome'],
    singleRun: false,
    client: {
      captureConsole: true
    },
    frameworks: ['mocha'],
    files: [
      'tests.webpack.js'
    ],
    preprocessors: {
      'tests.webpack.js': ['webpack']
    },
    reporters: ['dots'],
    webpack: {
      resolve: {
        root: path.resolve(__dirname, 'src'),
        extensions: ['', '.js', '.jsx']
      },
      module: {
        loaders: [
          {
            test: /\.jsx?$/,
            exclude: /node_modules/,
            loader: 'babel-loader'
          }
        ]
      },
      watch: true
    },
    webpackServer: {
      noInfo: true
    }
  })
}
