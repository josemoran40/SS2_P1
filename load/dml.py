Q1 = """
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
"""

Q2 = """
    select year_, STRING_AGG( ISNULL(name, ' '), ', ') as countries from (
    select distinct year_, country_.name from tsunami inner join location_ on location_.id = tsunami.id_location 
    inner join country_ on country_.id = location_.id_country group by year_, country_.name ) as t1 group by year_;
"""

Q3 = """
        select name, STRING_AGG( ISNULL(year_, ' '), ', ') as years from (
    select distinct year_, country_.name from tsunami inner join location_ on location_.id = tsunami.id_location 
    inner join country_ on country_.id = location_.id_country group by year_, country_.name ) as t1 group by name;
"""

Q4 = """
    select country_.name, AVG(isnull(damage.damage, 0)) as avgdamage from tsunami 
    inner join location_ on location_.id = tsunami.id_location 
    inner join country_ on country_.id = location_.id_country  
    inner join damage on damage.id = tsunami.id_damage
    group by country_.name order by avgdamage desc ;
"""

Q5 = """
    select Top 5 country_.name, sum(deaths.death) as deaths from tsunami 
    inner join location_ on location_.id = tsunami.id_location 
    inner join country_ on country_.id = location_.id_country  
    inner join deaths on deaths.id = tsunami.id_deaths
    group by country_.name order by deaths desc ;
"""

Q6 = """
    select Top 5 year_, sum(deaths.death) as deaths from tsunami 
    inner join deaths on deaths.id = tsunami.id_deaths
    group by year_ order by deaths desc ;
"""

Q7 = """
    select Top 5 year_, count(year_) as tsunamis from tsunami group by year_ order by tsunamis desc;
"""

Q8 = """
    select Top 5 country_.name, sum(houses.housesDestroyed) as destroyed from tsunami 
    inner join location_ on location_.id = tsunami.id_location 
    inner join country_ on country_.id = location_.id_country  
    inner join houses on houses.id = tsunami.id_houses
    group by country_.name order by destroyed desc ;
"""

Q9 = """
    select Top 5 country_.name, sum(houses.housesDamage) as damage from tsunami 
    inner join location_ on location_.id = tsunami.id_location 
    inner join country_ on country_.id = location_.id_country  
    inner join houses on houses.id = tsunami.id_houses
    group by country_.name order by damage desc ;
"""

Q10 = """
    select  AVG(isnull(maxWaterHeight, 0)) MaxWaterHeightAVG, country_.name from tsunami inner join location_ on location_.id = tsunami.id_location 
    inner join country_ on country_.id = location_.id_country where maxWaterHeight IS NOT NULL group by country_.name order by MaxWaterHeightAVG desc;
"""
