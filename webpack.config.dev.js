var webpack = require('webpack');
var _ = require('lodash');
var config = require('./webpack.config.base');
var path = require("path");

// var devConfig = _.merge(config, {

// });

var devConfig = _.merge(config, {
	output: {
			 path: path.resolve('./assets/bundles/'),
			 filename: "[name]-[hash].js",
	 },
 // 	devServer: {
 // 		port: 8080,
 // 		contentBase: "./static",
 // 		hot: true,
 // 		proxy: {
 // 			'*': 'http://172.16.252.128'
 // 		}
 // 	}
})

module.exports = devConfig;
