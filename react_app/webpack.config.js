var path = require('path')
var webpack = require('webpack')

module.exports = {
  devtool: 'eval',
  // entry: [
  //   'webpack-dev-server/client?http://localhost:3000',
  //   './src/index.jsx'
  // ],
  entry: {
    app: './src/index.jsx',
    vendor: [
      'ag-grid',
      'ag-grid-react',
      'axios',
      'd3',
      'highcharts',
      'highcharts-more',
      'lodash',
      'moment',
      'react',
      'react-addons-test-utils',
      'react-dom',
      'react-layer',
      'react-notification',
      'react-nprogress',
      'react-redux',
      'react-reorder',
      'react-router',
      'react-router-redux',
      'react-widgets',
      'redbox-react',
      'redux',
      'redux-actions',
      'redux-promise'
    ]
  },
  output: {
    path: path.join(__dirname, '../webapp/src/assets/js/'),
    filename: 'reactApp.js',
    publicPath: '../webapp/src/assets/js/'
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin('vendor', 'vendor.reactApp.js'),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin()
  ],
  resolve: {
    root: path.resolve(__dirname, 'src'),
    extensions: ['', '.js', '.jsx']
  },
  module: {
    loaders: [{
      test: /\.jsx?$/,
      loaders: ['babel'],
      include: path.join(__dirname, 'src')
    }]
  }
}
