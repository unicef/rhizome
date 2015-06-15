var webpack = require('webpack');
var _ = require('lodash');
var config = require('./webpack.config.base');

var devConfig = _.merge(config, {
	devServer: {
		port: 8080,
		contentBase: "./static",
		hot: true,
		proxy: {
			// Copy this file as webpack.config.dev.js
			// Then change this to the location of your local backend/VM
			'*': 'http://localhost:8000'
		}
	}
});

module.exports = devConfig;
