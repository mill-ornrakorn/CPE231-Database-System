DROP TABLE invoice_line_item;

CREATE TABLE invoice_line_item
(
    id integer,
    lineitem integer NOT NULL,
    invoice_no character varying(10) NOT NULL,
    product_code character varying(10) NOT NULL,
    quantity integer,
    unit_price numeric(18,2),
    extended_price numeric(18,2),
    CONSTRAINT invoice_line_item_pkey PRIMARY KEY (invoice_no, lineitem),
    CONSTRAINT invoice_line_item_product_product_code_fkey FOREIGN KEY (product_code)
        REFERENCES product (code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

DROP TABLE receipt_line_item;

CREATE TABLE receipt_line_item
(
    id integer,
    lineitem integer NOT NULL,
    receipt_no character varying(10),
    invoice_no character varying(10),
    amount_paid_here numeric(18,2),
    PRIMARY KEY (receipt_no, invoice_no),
    CONSTRAINT receipt_line_item_invoice_invoice_no_fkey FOREIGN KEY (invoice_no)
        REFERENCES invoice (invoice_no) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT receipt_line_item_receipt_receipt_no_fkey FOREIGN KEY (receipt_no)
        REFERENCES receipt (receipt_no) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION    
);

DROP TABLE payment_method;

CREATE TABLE payment_method (
    code character varying(10), 
    name character varying(100), 
    PRIMARY KEY (code)
);