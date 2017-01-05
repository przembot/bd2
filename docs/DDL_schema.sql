CREATE TABLE "Client" (
    "id" serial NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "surname" VARCHAR(255) NOT NULL,
    "birthdate" DATE NOT NULL,
    "address" TEXT NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "login" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    CONSTRAINT Client_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "Order" (
    "id" serial NOT NULL,
    "date" TIMESTAMP NOT NULL,
    "status" integer NOT NULL DEFAULT '0',
    "status_change_date" TIMESTAMP NOT NULL,
    "payment_status" integer NOT NULL,
    "client_id" integer NOT NULL,
    CONSTRAINT Order_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "Item" (
    "id" serial NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "price" DECIMAL NOT NULL,
    "description" TEXT NOT NULL,
    "in_stock" integer NOT NULL,
    "category_id" integer NOT NULL,
    CONSTRAINT Item_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "Review" (
    "id" serial NOT NULL,
    "rating" integer NOT NULL,
    "comment" TEXT NOT NULL,
    "date" TIMESTAMP NOT NULL,
    "client_id" integer NOT NULL,
    "item_id" integer NOT NULL,
    CONSTRAINT Review_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "Invoice" (
    "order_id" integer NOT NULL UNIQUE,
    "unique_no" integer NOT NULL UNIQUE,
    CONSTRAINT Invoice_pk PRIMARY KEY ("order_id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "Order_Item" (
    "id" serial NOT NULL,
    "quantity" integer NOT NULL,
    "price" DECIMAL NOT NULL,
    "order_id" integer NOT NULL,
    "item_id" integer NOT NULL,
    CONSTRAINT Order_Item_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "Employee" (
    "id" serial NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "surname" VARCHAR(255) NOT NULL,
    "pesel" VARCHAR(255) NOT NULL UNIQUE,
    "birthdate" DATE NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "address" VARCHAR(255) NOT NULL,
    "login" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    CONSTRAINT Employee_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "Category" (
    "id" serial NOT NULL,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    CONSTRAINT Category_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);


ALTER TABLE "Order"
      ADD CONSTRAINT "Order_fk0"
          FOREIGN KEY ("client_id")
          REFERENCES "Client"("id");

ALTER TABLE "Item"
      ADD CONSTRAINT "Item_fk0"
          FOREIGN KEY ("category_id")
          REFERENCES "Category"("id");

ALTER TABLE "Review"
      ADD CONSTRAINT "Review_fk0"
          FOREIGN KEY ("client_id")
          REFERENCES "Client"("id");

ALTER TABLE "Review"
      ADD CONSTRAINT "Review_fk1"
          FOREIGN KEY ("item_id")
          REFERENCES "Item"("id");

ALTER TABLE "Invoice"
      ADD CONSTRAINT "Invoice_fk0"
          FOREIGN KEY ("order_id")
          REFERENCES "Order"("id");

ALTER TABLE "Order_Item"
      ADD CONSTRAINT "Order_Item_fk0"
          FOREIGN KEY ("order_id")
          REFERENCES "Order"("id");

ALTER TABLE "Order_Item"
      ADD CONSTRAINT "Order_Item_fk1"
          FOREIGN KEY ("item_id")
          REFERENCES "Item"("id");
