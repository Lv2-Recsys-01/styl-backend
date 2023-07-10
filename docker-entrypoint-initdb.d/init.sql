-- BEGIN;


DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
    user_id SERIAL NOT NULL,
    user_name VARCHAR UNIQUE,
    user_pwd VARCHAR,
    PRIMARY KEY (user_id)
);


DROP TABLE IF EXISTS outfit;
CREATE TABLE outfit (
        outfit_id SERIAL NOT NULL,
        img_url VARCHAR,
        gender CHAR(1),
        age INTEGER,
        origin_url VARCHAR,
        reporter VARCHAR,
        tags VARCHAR[],
        brands VARCHAR[],
        region VARCHAR,
        occupation VARCHAR,
        style VARCHAR,
        "date" TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        PRIMARY KEY (outfit_id)
);


DROP TABLE IF EXISTS "session";
CREATE TABLE "session" (
        session_id VARCHAR PRIMARY KEY,
        user_id INTEGER REFERENCES "user" (user_id),
        created_at TIMESTAMP WITHOUT TIME ZONE,
        expired_at TIMESTAMP WITHOUT TIME ZONE
);


DROP TABLE IF EXISTS "like";
CREATE TABLE "like" (
        like_id SERIAL NOT NULL,
        session_id VARCHAR REFERENCES "session" (session_id),
        user_id INTEGER REFERENCES "user" (user_id),
        outfit_id INTEGER REFERENCES outfit (outfit_id),
        timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        is_deleted BOOLEAN,
        PRIMARY KEY (like_id)
);

DROP TABLE IF EXISTS click;
CREATE TABLE click (
        click_id SERIAL NOT NULL,
        session_id VARCHAR REFERENCES "session" (session_id),
        user_id INTEGER REFERENCES "user" (user_id),
        outfit_id INTEGER REFERENCES outfit (outfit_id),
        timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        duration_seconds INTEGER,
        PRIMARY KEY (click_id)
);

DROP TABLE IF EXISTS "similar";
CREATE TABLE "similar" (
        outfit_id INTEGER REFERENCES outfit (outfit_id),
        similar_outfits INTEGER[],
        PRIMARY KEY (outfit_id)
);


-- insert가 에러도 안 나고 로그에서도 "postgres    | INSERT 0 1" 이렇게 잘 됐다고 뜨는데 막상 db에 가보면 insert된 것이 없음. 그래서 우선은 직접 psql로 insert 해줌.
<<<<<<< HEAD
-- INSERT INTO "user" (user_name, user_pwd)
-- VALUES ('guest', 'guest_pwd');
=======
INSERT INTO "user" (user_name, user_pwd)
VALUES ('guest', 'guest_pwd');
>>>>>>> 98545f6177c416abca2b7175e164eff13dbbc126

-- INSERT INTO "user" (user_name, user_pwd)
-- VALUES ('guest2', 'guest_pwd2');


-- COMMIT;

-- COPY outfit (gender, age, img_url, origin_url, reporter, tags, brands, region, occupation, style, "date")
-- FROM '../meta_22-23.csv' DELIMITER ',' CSV HEADER;
