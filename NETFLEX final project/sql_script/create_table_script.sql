CREATE TABLE ACTOR(
    actor_id character varying(10),
    name character varying(30),
    gender character varying(5),
    PRIMARY KEY (actor_id)
);

CREATE TABLE PRODUCER(
    producer_id character varying(10),
    name character varying(20),
    gender character varying(5),
    PRIMARY KEY (producer_id)
);

CREATE TABLE CUSTOMER(
    customer_id character varying(10),
    first_name character varying(20),
    last_name character varying(20),
    phone_number integer,
    email character varying(20),
    password character varying(10),
    PRIMARY KEY (customer_id)
);

CREATE TABLE GENRE(
    genre_id character varying(10),
    genre_name character varying(20),
    PRIMARY KEY (genre_id)
);

CREATE TABLE MOVIE(
    movie_id character varying(10),
    movie_name character varying(100),
    title character varying(1000),
    genre_id character varying(10),
    copyright_date date,
    producer_id character varying(10),
    price numeric(10,2),
    image character varying(100),
    PRIMARY KEY (movie_id),
    CONSTRAINT genre_fkey FOREIGN KEY (genre_id)
        REFERENCES GENRE (genre_id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT movie_fkey FOREIGN KEY (movie_id)
        REFERENCES MOVIE (movie_id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT producer_fkey FOREIGN KEY (producer_id)
        REFERENCES PRODUCER (producer_id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE LIST_OF_ACTORS(
    actor_id character varying(10),
    movie_id character varying(10),
    PRIMARY KEY (actor_id, movie_id),
    CONSTRAINT actor_fkey FOREIGN KEY (actor_id)
        REFERENCES ACTOR (actor_id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT movie_fkey FOREIGN KEY (movie_id)
        REFERENCES MOVIE (movie_id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE "order"(
    customer_id character varying,
    movie_id character varying,
    day integer,
    PRIMARY KEY (customer_id, movie_id),
    CONSTRAINT customer_id FOREIGN KEY (customer_id)
        REFERENCES public.customer (customer_id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT movie_id FOREIGN KEY (movie_id)
        REFERENCES public.movie (movie_id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);