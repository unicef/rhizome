'use strict';

var _ = require('lodash');

var setAncestryArrayRecursive = function(ancestryArray,data){
   return _(data).forEach(function(value){
        value.ancestryArray = ancestryArray;
        if(value.children)
        {
          
          value.children = setAncestryArrayRecursive(ancestryArray.concat([value.title]), value.children);
        }
   }).value();
};

var setAncestryStringRecursive = function(ancestryString,data){
   return _(data).forEach(function(value){
        value.ancestryString = ancestryString + ' > ';
        if(value.children)
        {
          var descendentString = (ancestryString?ancestryString + ' > ' + value.title : value.title);
          value.children = setAncestryStringRecursive(descendentString, value.children);
        }
   }).value();
};

module.exports = function ancestry(data) {
	
	//var newData = setAncestryArrayRecursive([],data);
	var newData = setAncestryStringRecursive('',data);
	//console.log(newData);
	return newData;
};