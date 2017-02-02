# Marvel Character (and Universes) Statistics

This script scrapes data from [Marvel Wikia's](http://marvel.wikia.com/wiki/Marvel_Database) Characters category and creates a dataframe with info on which universes they have appeared, as well as how many characters have appeared in each one of them.

## Usage

'./generate-stats.py [n]', where n indicates the number of entries to consider when plotting graphs (defaults to 20).

## Results

### Analysis 1 - universes per character

First, the script creates a dataframe that shows the number of universes where a version of each character exists. Its most important statistical data are:

| Count | Mean | Std. Deviation |
|:-----:|:----:|:--------------:|
|2,7290 |1.83  |8.51            |

With the top 20 characters that appear in most universes, we can plot the following graphs:

![Universes per character](http://yandasilva.com/files/cbars.png)
![Universes per character](http://yandasilva.com/files/cbox.png)

Not surprisingly, Peter Parker is the character with most alternate versions (432), followed by Tony Stark (367) and Steve Rogers (350). It's interesting to note that 88.05% (24,030) of all 27,290 distinct Marvel Characters have appeared in only one universe. Also, Victor Van Doom is the only villain among the top 20 characters shown above.

### Analysis 2 - characters per universe

For the second analysis, the scripts creates a new dataframe showing how many characters have ever appeared in each of Marvel's universes, with the following statistical data:

| Count | Mean | Std. Deviation |
|:-----:|:----:|:--------------:|
|1,822  |27.39 |479.88          |

The following plots regard the 20 universes from which the most characters have come:

![Character](http://yandasilva.com/files/ubars.png)
![Character](http://yandasilva.com/files/ubox.png)

As expected, the main universe, Earth-616, has way more characters than the runner-up. Even though the most common observed value for the number of characters that come from a universe is 1, it happens only 25.80% of the times. This is consistent with the existance of many "What If..." universes, where multiple characters appear in a one-shot story, each one placed in an alternative universe.

It's also nice to notice that Earth-199999, also known as the Marvel Cinematic Universe (MCU), is already the fourth biggest universe, already surpassing universes that were home to famous storylines such as Days of Future Past, Age of Apocalypse or Earth X.
