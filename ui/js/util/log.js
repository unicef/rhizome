/* jshint unused: false */
'use strict';

var OFF = -1;
var ERR = 0;
var WRN = 1;
var INF = 2;
var LOG = 3;
var DBG = 4;

var loggers = ['error', 'warn', 'info', 'log', 'debug'];

function log(level, module) {
	if (typeof level !== 'number') {
		log.apply(null, [LOG].concat(arguments));
		return;
	}

	if (log.level < level) {
		return;
	}

	if (log.level < 0) {
		log(WRN, 'log', 'Invalid log level:', level);
		return;
	}

	var logger = console[loggers[level]] || console.log;
	var args   = Array.prototype.slice.call(arguments);

	logger.apply(console, [module + '::'].concat(args.slice(2)));
}

log.level = WRN;

log.error = function (module) {
	log.apply(null, [ERR].concat(Array.prototype.slice.call(arguments)));
};

log.warn = function (module) {
	log.apply(null, [WRN].concat(Array.prototype.slice.call(arguments)));
};

log.info = function (module) {
	log.apply(null, [INF].concat(Array.prototype.slice.call(arguments)));
};

log.debug = function (module) {
	log.apply(null, [DBG].concat(Array.prototype.slice.call(arguments)));
};

log.OFF = OFF;
log.ERR = ERR;
log.WRN = WRN;
log.INF = INF;
log.LOG = LOG;
log.DBG = DBG;

module.exports = log;
