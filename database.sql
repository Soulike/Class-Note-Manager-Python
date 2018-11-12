CREATE TABLE public.accounts
(
    id SERIAL PRIMARY KEY NOT NULL,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL
);
CREATE UNIQUE INDEX accounts_id_uindex ON public.accounts (id);
INSERT INTO public.accounts (id, username, password) VALUES (1, 'test', '85777f270ad7cf2a790981bbae3c4e484a1dc55e24a77390d692fbf1cffa12fa');
CREATE TABLE public.notes
(
    id SERIAL PRIMARY KEY NOT NULL,
    name varchar(255) NOT NULL,
    submit_time timestamp NOT NULL,
    last_update_time timestamp NOT NULL,
    account_id integer,
    CONSTRAINT account_id FOREIGN KEY (account_id) REFERENCES public.accounts (id)
);
CREATE UNIQUE INDEX note_id_uindex ON public.notes (id);
CREATE UNIQUE INDEX note_name_uindex ON public.notes (name);