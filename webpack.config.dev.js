var BundleTracker = require('webpack-bundle-tracker');
var webpack = require('webpack');
var config = require('./webpack.config.base');
var path = require("path");
var _ = require('lodash');


var devConfig = _.merge(config, {
	output: {
			 path: path.resolve('./assets/bundles/'),
			 filename: "main-[hash].js",
	     publicPath: '/static/',
	 },
	 plugins: [
		 new BundleTracker({filename: './webpack-stats.json'}),
		],

 // 	devServer: {
 // 		port: 8080,
 // 		contentBase: "./static",
 // 		hot: true,
 // 		proxy: {
 // 			'*': 'http://172.16.252.128'
 // 		}
 // 	}
});

module.exports = devConfig;
