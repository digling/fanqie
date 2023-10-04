function get_fanqie(fq){
  if (fq.length != 2) {
    return;
  }
  var shang, xia;
  [shang, xia] = fq;
  //console.log(shang, xia, fq, fanqie["shang"]["baxter"][shang])
  var b_i, b_m1, z_i, z_m1;
  try {
    [b_i, b_m1] = fanqie["shang"]["baxter"][shang][0];
    [z_i, z_m1] = fanqie["shang"]["zhou"][shang][0];
  }
  catch (e){
    [b_i, b_m1] = ["?", "?"];
    [z_i, z_m1] = ["?", "?"];
  }

  var b_m2, b_n, b_c, b_t, z_m2, z_n, z_c, z_t;
  try {
    [b_m2, b_n, b_c, b_t] = fanqie["xia"]["baxter"][xia][0];
    [z_m2, z_n, z_c, z_t] = fanqie["xia"]["zhou"][xia][0];
  }
  catch (e){
    [b_m2, b_n, b_c, b_t] = ["?", "?", "?", "?"];
    [z_m2, z_n, z_c, z_t] = ["?", "?", "?", "?"];
  }
  
  if (z_m1 != z_m2) {
    if (z_m2 == "." && z_m1 == "u") {
      z_m2 = "u"}
    else if (z_m2 == "." && z_m1 == "w") {
      z_m2 = "w"}
  }

  if (b_m1 != b_m2) {
    if (b_m2 == "." && b_m1 == "w") {
      b_m2 = "w"}
  }
  
  var b_out = [b_i, b_m2, b_n, b_c, b_t];
  var z_out = [z_i, z_m2, z_n, z_c, z_t];
  
  var i;
  var b_string, z_string;
  b_string = [];
  z_string = [];
  for (i=0; i<b_out.length; i++) {
    if (b_out[i] != ".") {
      b_string.push(b_out[i]);
    }
    if (z_out[i] != ".") {
      z_string.push(z_out[i]);
    }
  }

  var out = document.getElementById("output");
  var text = "<table>" +
    "<tr><th>Baxter (1992)</th><td>" +
    '<span class="char">' +
    b_string.join('</span> <span class="char">') +
    '</span>' +
    "</td></tr>" +
    "<tr><th>Zhōu (1958)</th><td>" +
    '<span class="char">' +
    z_string.join('</span> <span class="char">') +
    '</span>' +
    "</td></tr>" +
    "</table>";
  out.innerHTML = text;

  return [b_string.join(" "), z_string.join(" ")]
}

