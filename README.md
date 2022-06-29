# Made as an end of the year Advanced Script Languages project. Django + PostgreSQL + Bootstrap
Specification:

### Models: 
  Book:
    -ISBNs are unique and have length verification
    -author title and genre are unique together
    
  Film:
    -max quantity difference between genres are 3
    -if author and title are not unique together, then duration must be different
   
  CDs:
    -there cannot be two CD in the same genre, offering the same song list
    -CD of the same band can be offered in max 2 genres
   
### This app offers full CRUD using Django's Class-based Views. I have also implemented login and content verification based on user's group.
It also has renting system, statistics and user's details(rent date, return item).
Feel free to ask questions :)
    
