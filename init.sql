CREATE TABLE users (ID SERIAL PRIMARY KEY,
					login VARCHAR,
					password VARCHAR,
					name VARCHAR
				   );
				   
CREATE INDEX idx_check_login ON users (login);

CREATE INDEX idx_authorization ON users (login, password);

CREATE OR REPLACE PROCEDURE add_new_user(_login VARCHAR, _password VARCHAR, _name VARCHAR) AS $$
	BEGIN
		INSERT INTO users (login, password, name) VALUES
		(_login, _password, _name);
	END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION check_login (_login VARCHAR) RETURNS BOOLEAN AS $$
	BEGIN
	RETURN EXISTS(SELECT login FROM users WHERE login = _login);
	END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION authorization (_login VARCHAR, _password VARCHAR) RETURNS BOOLEAN AS $$
	BEGIN
	RETURN EXISTS(SELECT login FROM users WHERE (login = _login AND password = _password));
	END;
$$ LANGUAGE plpgsql;