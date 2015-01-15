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

	if (log.level >= level) {
		return;
	}

	if (log.level < 0) {
		log(WRN, 'log', 'Invalid log level:', level);
		return;
	}

	var logger = console[loggers[level]] || console.log;

	logger.apply(console, [module + '::'].concat(arguments.slice(2)));
}

log.level = WRN;

log.error = function (module) {
	log.apply(null, [ERR].concat(arguments));
};

log.warn = function (module) {
	log.apply(null, [WRN].concat(arguments));
};

log.info = function (module) {
	log.apply(null, [INF].concat(arguments));
};

log.debug = function (module) {
	log.apply(null, [DBG].concat(arguments));
};

log.OFF = OFF;
log.ERR = ERR;
log.WRN = WRN;
log.INF = INF;
log.LOG = LOG;
log.DBG = DBG;

module.exports = log;
