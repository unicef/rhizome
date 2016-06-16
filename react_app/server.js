var webpack = require('webpack')
var WebpackDevServer = require('webpack-dev-server')
var config = require('./webpack.config')

new WebpackDevServer(webpack(config), {
  publicPath: config.output.publicPath,
  historyApiFallback: true,
  hot: true,
  proxy: {
    '*': {
      target: 'http://localhost:8000',
      bypass: (req, res, proxyOptions) => {
        if (req.headers.accept.indexOf('html') !== -1) {
          console.log('Skipping proxy for browser request.')
          return '/index.html'
        }
      }
    }
  }
}).listen(3000, 'localhost', function (err, result) {
  if (err) {
    console.log(err)
  }

  console.log('Listening at localhost:3000')
})
