var webpack = require('webpack');
var _ = require('lodash');
var config = require('./webpack.config.base');

var distConfig = _.merge(config, {
	plugins: config.plugins.concat([
		new webpack.optimize.UglifyJsPlugin()
	])
});

module.exports = distConfig;
