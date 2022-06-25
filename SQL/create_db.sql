/**

"vocala-db"

postgresql
vocala 
version 0.1

**/

/**
CREATE DATABASE vocala_db
  WITH OWNER postgres
  TEMPLATE template0
  ENCODING 'UTF8';
  TABLESPACE vocala_data;
**/


/**

- change "foreign" in vocabularies to "non_native" because of name collision


**/

CREATE TABLE vc_vocabularies 
( id SERIAL UNIQUE,
  set_id INT NOT NULL,
  next_date DATE NOT NULL DEFAULT CURRENT_DATE,
  level INT NOT NULL DEFAULT 1 CONSTRAINT within_range CHECK ("level" <@ int4range(1,5)),
  native VARCHAR(256) NOT NULL,
  non_native VARCHAR(256) NOT NULL,
  description VARCHAR(128),
  FOREIGN KEY (set_id) REFERENCES vc_sets (id) ON DELETE CASCADE,
  PRIMARY KEY(id)
);



CREATE TABLE vc_users
( id SERIAL UNIQUE,
  username VARCHAR(32) UNIQUE NOT NULL,
  password VARCHAR(256) NOT NULL,
  email VARCHAR(256) UNIQUE NOT NULL,
  created_on TIMESTAMP NOT NULL,
  PRIMARY KEY(id) 
);


CREATE TABLE vc_sets
( id SERIAL UNIQUE,
  setname VARCHAR(256) NOT NULL,
  user_id INT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES vc_users (id) ON DELETE CASCADE,
  PRIMARY KEY(id) 
);

CREATE TABLE vc_usage_examples
( id SERIAL UNIQUE,
  example VARCHAR(256) NOT NULL,
  vocabulary_id INT NOT NULL,
  FOREIGN KEY (vocabulary_id) REFERENCES vc_vocabularies (id) ON DELETE CASCADE,
  PRIMARY KEY(id) );



/** adding tags 

- set int == serial ?!

- make better use of Timestamp in tables ? 

- create better user information ?

**/


/**

CREATE TYPE vocabulary_tag AS ENUM ('noun','adjective','verb','preposition','colloquial','adverb', 'pronoun', 'proverb', 'expression', 'abbreviation', 'other');


CREATE TABLE vc_vocabulary_tags
( id SERIAL UNIQUE,
  vocabulary_id INT NOT NULL,
  tag vocabulary_tag NOT NULL,
  FOREIGN KEY (vocabulary_id) references vc_vocabularies (id) ON DELETE CASCADE,
  PRIMARY KEY(id) );

  **/