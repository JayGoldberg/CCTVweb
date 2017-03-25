var fs = require('fs');

"use strict";

function bytesToHex(bytes) {

    for (var hex = [], i = 0; i < bytes.length; i++) {
        hex.push((bytes[i] >>> 4).toString(16));
        hex.push((bytes[i] & '0xF').toString(16));
	}
     return hex.join("");
}

function readcomment(buffer, pos) {
  //TODO(): a static length would prob help performance
  var commentString = [];

  for (true; pos < buffer.length; pos++) {
    if (buffer[pos] != '0xFF') {
      commentString.push(buffer[pos]);
    } else {
      break;
    };
  };
  return commentString;
}

function processJPEG (path) {
  const buflength = 300;
  var buffer = new Buffer(buflength);
  var comments;
  var MACaddr;
  var model;
  var JSONstring;
  
  fs.open(path, 'r', function(status, fd) {
    if (status) { console.error(status.message); return; };
    
	 		fs.read(fd, buffer, 0, buffer.length, 0, function(err, num) {
		 			comments = findCOMmarkers(buffer);
		 			MACaddr = bytesToHex(comments[0].slice(0,-1))
		 		 model = bytesToHex(comments[0].slice(-1))
			 		JSONstring = String.fromCharCode.apply(null, comments[1]);
			 		// check if either data piece is empty
			 		console.log('%s,%s,%s,%s', path, MACaddr, model, JSONstring);
			 		fs.close(fd);
		  });
	 });
};

function findCOMmarkers(buffer) {
  var comment = [];
  
  for (var i=0; i < buffer.length; i++) {
    if (buffer[i] == '0xFF') {
      if (buffer[i+1] == '0xFE') { // JPEG COM marker
        comment.push(readcomment(buffer, i+4));
      };
    };
  };
  return comment;
}

function walk(dir, done) {
  var results = [];
  
  fs.readdir(dir, function(err, list) {
    if (err) { return done(err); };
    
    var i = 0;
    (function next() {
      var file = list[i++];
      if (!file) { return done(null, results); };
      file = dir + '/' + file;
      fs.stat(file, function(err, stat) {
        if (stat && stat.isDirectory()) {
          walk(file, function(err, res) {
            results = results.concat(res);
            next();
          });
        } else {
          if (file.substr(-4).match(/(jpeg|jpg)/)) { processJPEG(file); }
          next();
        }
      });
    })();
  });
};

function usage() {
  console.log("usage here");
}

var args = process.argv.slice(2); // ignore $0 and $1 args

switch(args[0]) {
    case 'csvdump':
        walk(args[1], function(err, results) {
          if (err) { throw err; };
        });
        break;
    case 'dbwrite':
        break;
    case 'jpegdump':
        break;
    default:
        usage();
}
