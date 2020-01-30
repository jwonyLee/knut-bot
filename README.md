# knut-bot
텔레그램 봇

## Database
- PostgreSQL 11


### knut_bbs
| Column   | Type                   | Collation | Nullable | Default                                 |
|----------|------------------------|-----------|----------|-----------------------------------------|
| pk_id    | integer                |           | not null | nextval('knut_bbs_pk_id_seq'::regclass) |
| title    | character varying(100) |           | not null |                                         |
| category | character varying(100) |           |          |                                         |
| bbs_id   | character varying(200) |           | not null |                                         |
```SQL
create table knut_bbs (
	pk_id serial PRIMARY KEY,
	title varchar(100) UNIQUE not null,
	category varchar(100),
	bbs_id varchar(200) UNIQUE not null
);
```

### knut_article
| Column    | Type                   | Collation | Nullable | Default                                     |
|-----------|------------------------|-----------|----------|---------------------------------------------|
| pk_id     | integer                |           | not null | nextval('knut_article_pk_id_seq'::regclass) |
| bbs_title | character varying(100) |           |          |                                             |
| title     | character varying(300) |           | not null |                                             |
| link      | character varying(300) |           | not null |                                             |

```SQL
create table knut_article (
	pk_id serial PRIMARY KEY,
	bbs_title varchar(100) REFERENCES knut_bbs (title),
	title varchar(300) not null,
	link varchar(300) not null
);
```
