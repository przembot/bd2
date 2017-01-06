function getCookie(c_name)
{
  if (document.cookie.length > 0) {
    c_start = document.cookie.indexOf(c_name + "=");
    if (c_start != -1) {
      c_start = c_start + c_name.length + 1;
      c_end = document.cookie.indexOf(";", c_start);
      if (c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start,c_end));
    }
  }
  return "";
}

$(document).ready(function() {
  $.ajaxSetup({
    headers: { "X-CSRFToken": getCookie("csrftoken") }
  });
  cart = loadCart();
  if (cart == null)
    newCart();
  repaintCart();
});


// Usuwa aktualnie narysowany koszyk
// i rysuje na nowo go
function repaintCart() {
  data = listItems();
  sum = data.reduce(function(acc, a) {
    return acc + (a.price*a.amount);
  }, 0.0).toFixed(2);
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

// Wysyla zamowienie do serwera
function sendOrder() {
  order = new Object();
  items = listItems();
  items = items.map(function(i) {
    var e = new Object();
    e.id = i.id;
    e.amount = i.amount;
    return e;
  });
  order.invoice = false; //TODO - sprawdz czy klient chce fakture
  order.items = items;
  sendOrderRequest(order, function() { // success
    alert("Zamówienie złożone pomyślnie!");
    newCart();
    repaintCart();
  }, sendOrderError);
}

// Wysyla zapytanie tworzace zamowienie
function sendOrderRequest(order, onSuccess, onError)
{
  $.ajax(
    { url: '/order/'
    , success: onSuccess
    , data: JSON.stringify(order)
    , contentType: 'application/json'
    , error: onError
    , type: 'POST'
    });
}

// Przetwarza sytuacje bledna wynikla w przypadku skladania zamowienia
function sendOrderError(xhr, textstatus) {
  if (xhr.status == 401) {
    window.location.replace("/login");
  } else if (xhr.status == 400) {
    alert("Zamówienie nie może zostać zrealizowanie");
  } else {
    alert("Zamówienie nieudane :(");
  }
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
  str += "zł</strong></h4><button onclick=\"sendOrder()\" type=\"button\" class=\"btn btn-success btn-md\">";
  str += "<span class=\"glyphicon glyphicon-ok\"></span> Zatwierdź</button>";
  return str;
}
