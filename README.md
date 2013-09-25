wordassoc-flask-feeback
=======================

A collection of anonymized user data and a simple python script performing analysis to drive user feedback

## Requirements

1. Python 2.7 (may be 3.x compatible, but untested)
2. Numpy
3. (Optional) Matplotlib

## To Run
1. ```> python analysis.py```

## Usage Demographics

	Total number of answers: 494
	Total number of players: 29
	Average number of wrong answers per game: 6.75862068966
	Average number of right answers per game: 10.275862069

## Game Analysis

	Number of games per technology
		java : 23
		c/c++ : 12
		matlab : 8
		git : 6
		python : 6
		javascript : 5
		c# : 4
		----------------------------------------------------
		Most popular tech -  java : 23
		Least popular tech - c# : 4
		----------------------------------------------------

	Percentage of correct answers by category:
		javascript : 0.454545454545
		git : 0.357142857143
		general programming principles : 0.352112676056
		java : 0.328358208955
		matlab : 0.296296296296
		c/c++ : 0.28125
		c# : 0.25
		algorithm runtime : 0.243243243243
		data structure identification : 0.241758241758
		object-oriented design identification : 0.233766233766
		python : 0.222222222222
		----------------------------------------------------
		Best category - javascript : 0.454545454545
		Worst category - python : 0.222222222222
		----------------------------------------------------

	Question accuracy by question:
		--------------------
		Best question not everyone got right - `Foo extends Bar` : 0.888888888889
		Worst question someone got right - `index` : 0.0909090909091
		--------------------

	Distribution of Number of Correctly Answered Questions by Game:
		[3 6 3 8 3 0 1 1 2 1]
		[  5.    6.6   8.2   9.8  11.4  13.   14.6  16.2  17.8  19.4  21. ]

	Distribution of Number of Answered Questions by Game:
		[4 6 7 4 1 1 2 1 0 2]
		[ 13.   14.5  16.   17.5  19.   20.5  22.   23.5  25.   26.5  28. ]
