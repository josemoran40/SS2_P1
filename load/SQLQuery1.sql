use tsunami_historical;

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
			damage varchar(50),
			damageDescription int,
			housesDestroyed int,
			housesDamage int
			);

select * from temp;

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
			damage varchar(50),
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


truncate table tsunami;

select distinct * from temp left join deaths on temp.deaths = deaths.death;

select distinct id_missing from tsunami; 

select * from deaths where id = 33;
select * from injuries where id = 22;

select * from location_;

select * from damage where id = 68;
select * from tsunami where id_damage = 68;

select deaths.id, deaths.death from temp left join deaths on temp.deaths = deaths.death;

select * from deaths where id = 102;

select * from tsunami;

select * from damage;

select * from damage where damage.damage = 0.005;


select distinct year_, STRING_AGG( ISNULL(country_.name, ' '), ', ') as countries from tsunami inner join location_ on location_.id = tsunami.id_location 
inner join country_ on country_.id = location_.id_country group by year_ ;


select year_, STRING_AGG( ISNULL(name, ' '), ', ') as countries from (
select distinct year_, country_.name from tsunami inner join location_ on location_.id = tsunami.id_location 
inner join country_ on country_.id = location_.id_country group by year_, country_.name ) as t1 group by year_;

select name, STRING_AGG( ISNULL(year_, ' '), ', ') as years from (
select distinct year_, country_.name from tsunami inner join location_ on location_.id = tsunami.id_location 
inner join country_ on country_.id = location_.id_country group by year_, country_.name ) as t1 group by name;


select Top 5 country_.name, sum(deaths.death) as deaths from tsunami 
inner join location_ on location_.id = tsunami.id_location 
inner join country_ on country_.id = location_.id_country  
inner join deaths on deaths.id = tsunami.id_deaths
group by country_.name order by deaths desc ;



select Top 5 year_, sum(deaths.death) as deaths from tsunami 
inner join deaths on deaths.id = tsunami.id_deaths
group by year_ order by deaths desc ;


select Top 5 year_, count(year_) as tsunamis from tsunami group by year_ order by tsunamis desc;

select Top 5 country_.name, sum(houses.housesDestroyed) as destroyed from tsunami 
inner join location_ on location_.id = tsunami.id_location 
inner join country_ on country_.id = location_.id_country  
inner join houses on houses.id = tsunami.id_houses
group by country_.name order by destroyed desc ;

select Top 5 country_.name, sum(houses.housesDamage) as damage from tsunami 
inner join location_ on location_.id = tsunami.id_location 
inner join country_ on country_.id = location_.id_country  
inner join houses on houses.id = tsunami.id_houses
group by country_.name order by damage desc ;

select  AVG(isnull(maxWaterHeight, 0)) MaxWaterHeightAVG, country_.name from tsunami inner join location_ on location_.id = tsunami.id_location 
inner join country_ on country_.id = location_.id_country where maxWaterHeight IS NOT NULL group by country_.name order by MaxWaterHeightAVG desc;




select * from tsunami where id_damage=29;


drop table temp;
drop table tsunami;
drop table damage;
drop table location_;
drop table country_;
drop table injuries;
drop table missing;
drop table houses;
drop table deaths;


select * from temp;
select 'Tsunami' as name, COUNT(*) as count from tsunami
union
select 'Damage' as name, COUNT(*) as count from damage
union
select 'Houses' as name, COUNT(*) as count from houses
union
select 'Injuries' as name, COUNT(*) as count from injuries
union
select 'Missings' as name, COUNT(*) as count from missing
union
select 'Countries' as name, COUNT(*) as count from country_
union
select 'Locations' as name, COUNT(*) as count from location_;


select country_.name, AVG(isnull(damage.damage, 0)) as avgdamage from tsunami 
inner join location_ on location_.id = tsunami.id_location 
inner join country_ on country_.id = location_.id_country  
inner join damage on damage.id = tsunami.id_damage
group by country_.name order by avgdamage desc ;

select * from tsunami;