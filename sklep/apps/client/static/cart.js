// Note - koszyk jest pamietany na czas sesji

// Koszyk sklada sie z listy itemow
// Item : { id: Int, name : string, price: Int, amount: Int }
//
// Udostepnione funkcjonalnosci dla koszyka
// newCart() - tworzy nowy koszyk (lub wyczyszcza poprzedni, jesli istnial)
// addItem(id : Int, name : String, price: Int, amount : Int) -
//    dodaje nowy przedmiot do koszyka
//    dzialanie koszyka dla amount <= 0 jest nieokreslone (!)
// removeItem(id) - usuwa item z koszyka o podanym id
// addAmount(id) - dodaje o jeden ilosc itemu w koszyku
//    jesli nie istnial wczesniej item - nie dzieje sie nic
// deleteAmount(id) - usuwa o jeden ilosc itemu w koszyku
//    jesli po odjeciu jest 0 wystapien - przedmiot usuwa sie z koszyka
// listItems() - wypisuje liste przedmiotow bedacych aktualnie w koszyku
//    przedmioty opisane sa jak wyzej objekt Item
// generateOrder(isInvoiceRequired) - generuje stringa bedacego zapytaniem
//    tworzacym zamowienie w systemie
//    parametr typu boolean - okresla, czy klient chce fakture

// Czysci lub tworzy koszyk, jesli jeszcze nie powstal
function newCart() {
  var cart = new Object();
  cart.items = [];
  storeCart(cart);
}

// Zapisuje koszyk do przegladarki
function storeCart(cart) {
  window.localStorage.setItem("cart", JSON.stringify(cart));
}

// Odczytuje aktualny koszyk
function loadCart() {
  return JSON.parse(window.localStorage.getItem("cart"));
}

function hasItem(id) {
  return function(item) {
    return item.id === id;
  }
}

// Dodaje przedmiot do koszyka
// Jesli istnieje juz dany przedmiot, dodaje podana ilosc produktu
function addItem(id, name, price, amount) {
  cart = loadCart();
  if (cart.items.find(function(item) { return item.id === id }) != undefined) {
    cart.items.map(function(item) {
      if (item.id == id)
        item.amount += amount;
      return item;
    });
    storeCart(cart);
    return;
  }

  var item = new Object();
  item.id = id;
  item.name = name;
  item.price = price;
  item.amount = amount;
  cart.items.push(item);
  storeCart(cart);
}

// Usuwa przedmioty z koszyka o danym id
// jesli nie istnieje - nie robi nic
function removeItem(id) {
  cart = loadCart();

  cart.items = cart.items.filter(function(item) { return item.id != id; });
  storeCart(cart);
}


// Dodaje o jeden ilosc zamawianego danego przedmiotu
// jesli nie istnieje dany przedmiot w koszyku - nie robi nic
function addAmount(id) {
  cart = loadCart();

  cart.items = cart.items.map(function(item) {
    if(item.id === id)
      item.amount += 1;
    return item;
  });

  storeCart(cart);
}


// Funkcja pomocnicza
function delAmount(id) {
  return function(result, current) {
    if(current.id === id) {
      if(current.amount > 1) {
        current.amount -= 1;
        result.push(current);
        return result;
      }
    } else {
      result.push(current);
      return result;
    }
    return result;
  };
}

// Zmniejsza o jeden ilosc zamawianego danego produktu
// jesli zmieni sie na 0 - usuwa przedmiot z koszyka
function deleteAmount(id) {
  cart = loadCart();

  cart.items = cart.items.reduce(delAmount(id), []);

  storeCart(cart);
}

// Zwraca liste przedmiotow bedaca aktualnie w koszyku
function listItems() {
  cart = loadCart();
  return cart.items;
}


// Przetwarza format danych z koszyka na format do zamowienia
function cartItemToItemSpec(cartItem) {
  var itemspec = new Object();
  itemspec.id = cartItem.id;
  itemspec.amount = cartItem.amount;
  return itemspec;
}


// Zwraca stringa bedacego zapytaniem do serwera o utworzenie zapytanie
function generateOrder(isInvoiceRequired) {
  cart = loadCart();
  var order = new Object();
  order.faktura = isInvoiceRequired;
  order.items = cart.items.map(cartItemToItemSpec);
  return JSON.stringify(order);
}

// Prosty test

/*
newCart();
addItem(1, "Kotek", 2);
addItem(2, "Piesek", 4);
addAmount(2);
deleteAmount(1);
deleteAmount(1);
deleteAmount(2);
console.log(generateOrder(true));
*/

//koszyk powinien zawierac 4 pieski
