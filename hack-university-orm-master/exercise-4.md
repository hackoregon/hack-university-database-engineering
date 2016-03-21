# Exercise 4 - aggregations


## Part 1 - AVG, MIN, MAX

The Django ORM requires its aggregations to be imported and use the following syntax

    from django.db.models import Avg, Min, Max, Sum, Count
    
    Ship.objects.all().aggregate(Avg('capacity'))

What is the total capacity of all the ships in the fleet?

## Part 2 - Group By

Group By maps to the `Count` aggregation with the Django ORM using the following syntax

    Crimedataraw.objects.values('neighborhood').annotate(Count('neighborhood'))

How many logs are there per ship?

    Hint: In the example above, if neightborhood was a foreign key relation, `values(neighborhood__name)` would display the name of the neighborhood instead of its id.

How many captain's logs?
