CREATE_TABLE = """
            CREATE TABLE temp (
                        id int IDENTITY(1,1) PRIMARY KEY,
                        year_ int,
                        month_ int,
                        day_ int,
                        hour_ int,
                        min_ int,
                        sec_ int,
                        event_validity int,
                        cause_code int,
                        magnitud DECIMAL(5,2),
                        deposits int,
                        country varchar(200),
                        location_ varchar(500),
                        latitude varchar(10),
                        longuitude varchar(10),
                        maxWaterHeight DECIMAL(5,2),
                        runups int,
                        tsunameMagnitud varchar(10),
                        intensity varchar(10),
                        deaths int,
                        missing int,
                        missingDescription int,
                        injuries int,
                        damage DECIMAL(10,4),
                        damageDescription int,
                        housesDestroyed int,
                        housesDamage int
                        );

            create table country_ (
                        id int IDENTITY(1,1) PRIMARY KEY,
                        name varchar(500)
                        );

            create table location_ (
                        id int IDENTITY(1,1) PRIMARY KEY,
                        name varchar(500),
                        id_country int,
                        FOREIGN KEY (id_country) REFERENCES country_(id)
                        );

            create table damage(
                        id int IDENTITY(1,1) PRIMARY KEY,
                        damage DECIMAL(10,4),
                        damageDescription int
            );


            create table houses(
                        id int IDENTITY(1,1) PRIMARY KEY,
                        housesDestroyed int,
                        housesDamage int
            );

            create table missing(
                        id int IDENTITY(1,1) PRIMARY KEY,
                        missing int,
                        missingDescription int
            )


            create table deaths(
                        id int IDENTITY(1,1) PRIMARY KEY,
                        death int
            )

            create table injuries(
                        id int IDENTITY(1,1) PRIMARY KEY,
                        injurie int
            )


            create table tsunami(
            id int IDENTITY(1,1) PRIMARY KEY,
                        year_ int,
                        month_ int,
                        day_ int,
                        hour_ int,
                        min_ int,
                        sec_ int,
                        event_validity int,
                        cause_code int,
                        magnitud DECIMAL(5,2),
                        deposits int,
                        latitude varchar(10),
                        longuitude varchar(10),
                        maxWaterHeight DECIMAL(5,2),
                        runups int,
                        tsunameMagnitud varchar(10),
                        intensity varchar(10),
                        id_location int,
                        id_deaths int,
                        id_injuries int,
                        id_damage int,
                        id_missing int,
                        id_houses int,
                        FOREIGN KEY (id_location) REFERENCES location_(id),
                        FOREIGN KEY (id_deaths) REFERENCES deaths(id),
                        FOREIGN KEY (id_injuries) REFERENCES injuries(id),
                        FOREIGN KEY (id_damage) REFERENCES damage(id),
                        FOREIGN KEY (id_missing) REFERENCES missing(id),
                        FOREIGN KEY (id_houses) REFERENCES houses(id)
            ); 
        """

DROP_TABLE = """  
        drop table temp;
        drop table tsunami;
        drop table damage;
        drop table location_;
        drop table country_;
        drop table injuries;
        drop table missing;
        drop table houses;
        drop table deaths;
"""

BULK_LOAD = """
        insert into country_(name)	
        select distinct country from temp;

        insert into location_(name, id_country)	
        select distinct temp.location_, country_.id from temp left join country_ on temp.country =  country_.name;

        insert into damage
        select distinct temp.damage, temp.damageDescription from temp;

        insert into houses
        select distinct temp.housesDestroyed, temp.housesDamage from temp;

        insert into missing
        select distinct temp.missing,temp.missingDescription from temp;

        insert into deaths
        select distinct temp.deaths from temp;

        insert into injuries
        select distinct temp.injuries from temp;


        insert into tsunami(year_, month_, day_, hour_, min_, sec_, event_validity, cause_code, magnitud, 
	deposits, latitude, longuitude,maxWaterHeight,runups,intensity, id_location, id_deaths, id_injuries, id_damage, id_missing,
	id_houses)
	select distinct temp.year_, temp.month_,temp.day_,temp.hour_, temp.min_,temp.sec_,temp.event_validity,
	temp.cause_code, temp.magnitud, temp.deposits, 
	 temp.latitude, temp.longuitude, temp.maxWaterHeight, temp.runups, temp.intensity,
	location_.id, deaths.id, injuries.id, damage.id, missing.id, houses.id from temp
	left join location_ on location_.name = temp.location_
	left join country_ on country_.name = temp.country
	left join deaths on isnull(temp.deaths,777666) = isnull(deaths.death,777666)
	left join injuries on isnull(temp.injuries,777666) = isnull(injuries.injurie,777666)
	left join damage on (isnull(temp.damage,777666) = isnull(damage.damage,777666) and 
				isnull(temp.damageDescription,777666) = isnull(damage.damageDescription,777666)) 
	left join missing on (isnull(temp.missing,777666) = isnull(missing.missing,777666) and isnull(temp.missingDescription,777666) = isnull(missing.missingDescription,777666)) 
	left join houses on (isnull(temp.housesDestroyed,777666) = isnull(houses.housesDestroyed,777666) and isnull(temp.housesDamage,777666) = isnull(houses.housesDamage,777666)) 
	where location_.id_country = country_.id;
"""
