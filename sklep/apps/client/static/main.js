$(document).ready(function() {
  repaintCart();
});


// Usuwa aktualnie narysowany koszyk
// i rysuje na nowo go
function repaintCart() {
  data = listItems();
  sum = data.reduce(function(acc, a) {
    return acc + (a.price*a.amount);
  }, 0.0);
  data = data.map(function(item) {
    return genOneItemHtml(item.id, item.name, item.price, item.amount);
  });
  data.join();
  $("#cartinfo").html(data);

  sum = genSumHtml(sum);
  $("#cartsum").html(sum);
}

// Dodaje przedmiot do koszyka i odswieza go
function cartAdd(id, name, price) {
  addItem(id, name, price, 1);
  repaintCart();
}

// Usuwa przedmiot z koszyka i odswieza go
function cartRemove(id) {
  removeItem(id);
  repaintCart();
}


function genOneItemHtml(id, name, price, amount) {
  var str = "<div class=\"row\"><div class=\"col-md-4\"><h5 class=\"product-name\"><strong>";
  str += name;
  str += " </strong></h5></div><div class=\"col-md-2\"><h6><strong>"
  str += price;
  str += "zł </strong></h6></div><div class=\"col-md-2\"><h6><span class=\"text-muted\">x </span>";
  str += amount;
  str += "</h6></div><div class=\"col-md-1\"><button type=\"button\" onclick=\"cartRemove("+id+")\" class=\"btn btn-link btn-md\">";
  str += "<span class=\"glyphicon glyphicon-trash\"> </span></button></div></div><hr>";
  return str;
}


function genSumHtml(sum) {
  var str = "<h4 class=\"text-center\">Łącznie <strong>";
  str += sum;
  str += "zł</strong></h4><button type=\"button\" class=\"btn btn-success btn-md\">";
  str += "<span class=\"glyphicon glyphicon-ok\"></span> Zatwierdź</button>";
  return str;
}
