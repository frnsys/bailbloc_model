function log(d) {
  var p = document.createElement('p');
  p.innerHTML = JSON.stringify(d);
  document.body.append(p);
}

var worker = new Worker('worker.js');
worker.onmessage = function(m) {
  var results = m.data;
  log(results);
};
