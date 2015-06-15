var webpack = require('webpack');
var _ = require('lodash');
var config = require('./webpack.config.base');

var devConfig = _.merge(config, {
	devServer: {
		port: 8080,
		contentBase: "./static",
		hot: true,
		proxy: {
			'*': 'http://172.16.252.128'
		}
	}
});

module.exports = devConfig;
