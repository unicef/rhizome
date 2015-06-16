var path = require('path');
var webpack = require('webpack');

module.exports = {
	context: __dirname,
	entry: {
		app: './ui/js/PolioScape.js',
		vendor: ['react', 'vue', 'd3', 'reflux', 'superagent']
	},
	output: {
		path: path.join(__dirname, 'static'),
		publicPath: '/static/',
		filename: 'main.js',
		// export main.js as global var `Polio`
		libraryTarget: 'var',
		library: "Polio"
	},

	devtool: 'source-map',

	plugins: [
		new webpack.NoErrorsPlugin(),
		new webpack.optimize.CommonsChunkPlugin('vendor', 'vendor.js'),
		new webpack.optimize.DedupePlugin()
	],
	resolve: {
		modulesDirectories: ['node_modules', 'ui/js'],
		// alias so that npm linked modules can't instantiate a 2nd react instance (bad bad)
		// this is broken now with webpack update for some reason... todo: figure out why
		//alias: {
		//	"react": "node_modules/react/react.js"
		//},
		extensions: ['', '.js', '.jsx', '.html']
	},
	module: {
		loaders: [
			{
				// transpile JS and JSX files with Babel
				test: /\.jsx?$/,
				loaders: ['babel-loader'],
				exclude: /node_modules/
			},
			{
				// bundle html imports as text strings
				test: /\.html$/,
				loaders: ['html']
			}
		]
	}
};
