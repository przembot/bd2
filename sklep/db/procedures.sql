-- Function: public.get_categories()

-- DROP FUNCTION public.get_categories();

CREATE OR REPLACE FUNCTION public.get_categories()
  RETURNS SETOF dao_category AS
$BODY$ SELECT * FROM dao_category
$BODY$
  LANGUAGE sql IMMUTABLE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.get_categories()
  OWNER TO postgres;

  
-- Function: public.get_item_by_id(integer)

-- DROP FUNCTION public.get_item_by_id(integer);

CREATE OR REPLACE FUNCTION public.get_item_by_id(_item_id integer)
  RETURNS SETOF dao_item AS
$BODY$
BEGIN
	RETURN QUERY
	SELECT *
	FROM dao_item AS doi
	WHERE doi.id = _item_id;
	
END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.get_item_by_id(integer)
  OWNER TO postgres;


-- Function: public.get_items_by_category_id(integer)

-- DROP FUNCTION public.get_items_by_category_id(integer);

CREATE OR REPLACE FUNCTION public.get_items_by_category_id(_category_id integer)
  RETURNS SETOF dao_item AS
$BODY$ SELECT * FROM dao_item WHERE category_id_id = _category_id
$BODY$
  LANGUAGE sql IMMUTABLE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.get_items_by_category_id(integer)
  OWNER TO postgres;

 
-- Function: public.get_orders_sum_by_client_id(integer)

-- DROP FUNCTION public.get_orders_sum_by_client_id(integer);

CREATE OR REPLACE FUNCTION public.get_orders_sum_by_client_id(IN _client_id integer)
  RETURNS TABLE(order_id integer, order_sum numeric) AS
$BODY$
BEGIN
	RETURN QUERY
	SELECT order_id_id, quantity*price 
	FROM dao_order AS daor
		JOIN dao_order_item AS doi
			ON daor.id = doi.order_id_id 
		JOIN accounts_client AS ac
			ON ac.user_id = daor.client_id_id
		WHERE ac.user_id = _client_id;
	
END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.get_orders_sum_by_client_id(integer)
  OWNER TO postgres;

SELECT * FROM get_orders_sum_by_client_id(16);


-- Function: public.get_orders_by_client_id(integer)

-- DROP FUNCTION public.get_orders_by_client_id(integer);

CREATE OR REPLACE FUNCTION public.get_orders_by_client_id(IN _client_id integer)
  RETURNS TABLE(id integer, date timestamp with time zone, status integer) AS
$BODY$
BEGIN
	RETURN QUERY
	SELECT daor.id, daor.date, daor.status 
	FROM dao_order AS daor
		JOIN accounts_client AS ac
			ON ac.user_id = daor.client_id_id
	WHERE ac.user_id = 16;
	
END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.get_orders_by_client_id(integer)
  OWNER TO postgres;

-- Function: public.get_reviews_by_item_id(integer)

-- DROP FUNCTION public.get_reviews_by_item_id(integer);

CREATE OR REPLACE FUNCTION public.get_reviews_by_item_id(IN _item_id integer)
  RETURNS TABLE(username character varying, date timestamp with time zone, rating integer, comment text) AS
$BODY$
BEGIN
	RETURN QUERY
	SELECT accust.username AS username, dr.date AS date, dr.rating AS rating, dr.comment AS comment  
	FROM dao_item AS doi
		LEFT JOIN dao_review dr
			ON doi.id = dr.item_id_id
		LEFT JOIN accounts_client AS ac
			ON ac.user_id = dr.client_id_id
		JOIN accounts_customuser AS accust
			ON accust.id = ac.user_id
	WHERE doi.id = _item_id;
	
END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.get_reviews_by_item_id(integer)
  OWNER TO postgres;
  
  
-- Type: public.order_detail

-- DROP TYPE public.order_detail;

CREATE TYPE public.order_detail AS
   (item_id integer,
    quantity integer);
ALTER TYPE public.order_detail
  OWNER TO postgres;
  
-- Function: public.make_order(integer, order_detail[])

-- DROP FUNCTION public.make_order(integer, order_detail[]);

CREATE OR REPLACE FUNCTION public.make_order(
    _client_id integer,
    _order_details order_detail[])
  RETURNS void AS
$BODY$
DECLARE _order_id integer;
	_order_item order_detail;
	_item_price numeric;
BEGIN
	--First check if all items in order are available
	FOREACH _order_item IN ARRAY _order_details
	LOOP
		IF (SELECT COUNT(*) FROM dao_item AS di
			WHERE di.id = _order_item.item_id
			AND di.in_stock < _order_item.quantity)
		THEN
			RAISE EXCEPTION 'Item quantity too low';
		END IF;
	END LOOP;

	--all items available	
	INSERT INTO dao_order (date, status, status_change_date, payment_status, client_id_id)
		VALUES(now(), 0, now(), 0, _client_id) RETURNING id INTO _order_id;
	
	FOREACH _order_item IN ARRAY _order_details
	LOOP
		SELECT price FROM dao_item AS di
			WHERE di.id = _order_item.item_id 
			INTO _item_price;
		RAISE NOTICE 'quantity %, price %, item_id_id %, order_id_id %', 
			_order_item.quantity, _item_price, _order_item.item_id, _order_id;
		INSERT INTO dao_order_item(quantity, price, item_id_id, order_id_id)
			VALUES (_order_item.quantity, _item_price, _order_item.item_id, _order_id);

		UPDATE dao_item AS di SET in_stock = (di.in_stock - _order_item.quantity)
			WHERE di.id = _order_item.item_id;
	END LOOP;
	
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.make_order(integer, order_detail[])
  OWNER TO postgres;
  

SELECT make_order(16, array[row(16,1)::order_detail, row(17, 2)::order_detail]);

