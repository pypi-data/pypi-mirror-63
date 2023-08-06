# Random PESEL

Random PESEL number generator.

PESEL is the national identification number used in Poland.


## Instalation
    pip3 install random-pesel


## Usage

    from random_pesel import RandomPESEL
    pesel = RandomPESEL()
    
    # Generate random PESEL number
    pesel.generate()
    
    # Generate random male PESEL number
    pesel.generate(gender='m')
    
    # Generate random female PESEL number
    pesel.generate(gender='f')
    
    # Generate random PESEL number with min age defined
    pesel.generate(min_age=18)
    
    # Generate random PESEL number with max age defined
    pesel.generate(max_age=30)

