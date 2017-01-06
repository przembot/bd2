-- Function: public.move_items_from_category_to_default()

-- DROP FUNCTION public.move_items_from_category_to_default();

CREATE OR REPLACE FUNCTION public.move_items_from_category_to_default()
  RETURNS trigger AS
$BODY$
BEGIN
	UPDATE dao_item AS di SET category_id_id = 11 
		WHERE di.category_id_id = OLD.id;
	RETURN old;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.move_items_from_category_to_default()
  OWNER TO postgres;

 
CREATE TRIGGER move_items_from_category_on_delete BEFORE DELETE ON dao_category
	FOR EACH ROW EXECUTE PROCEDURE move_items_from_category_to_default();