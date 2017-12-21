var fs = require('fs');

var info = {};

var lines = fs.readFileSync('/proc/cpuinfo').toString().split('\n');
for(line in lines) {
    var parts=lines[line].replace(/\t/g, '').split(':');

    if (parts.length == 2) {
        var key=parts[0];
        var value=parts[1].trim();
        if (key === 'Serial') {
            info.serial = value;
        } else if (key === 'Hardware') {
            info.hardware = value;
        } else if (key === 'Revision') {
            info.revision = value;
        }
    }
}

console.log("info", info);
