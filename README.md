# adv

A quick-and-dirty command line script for helping with advising tasks.

The `data/` directory should contain `glasgow.json`. There is a scraper script in there as well to regenerate, if necessary.

The main functionality is as follows:

  * Course name lookup from code. For example, `./adv.py -n 4021` or `./adv.py -n compsci4021` will give back "Functional Programming (H)".
  * Course code lookup from name. This also includes common aliases for courses. For example, `./adv.py -c fp` or `./adv.py -c functional` will give `COMPSCI4021`.
  * Aggregation over a set of weighted components of a course. For example to calculate the overall course grade from two components, the first as an A2 weighted at 80% and the second as a C2 weighted at 20%, we would write `./adv.py -cagg a2@80 c2@20` which will result in 19.4 = A4.
  * Aggregation over a credit-weighted set of courses. Any course without a credit weighting will default to 10. So for example to calculate a 4th-year GPA where the individual project is weighted as 40 and the remainder are 10, we can do `./adv.py -agg a2@40 b1 b2 b3 b3 b3 b3 e1 e2` which would result in an aggregated grade of B2.
  * Conversion from a letter grade to a grade point: `./adv.py -gpa a2` would result in 21.
  * Conversion from a grade point to a letter grade: `./adv.py -g 21` would result in B2.

## Summary:
  * Course name lookup: `./adv.py -n <course code>`
  * Course code lookup: `./adv.py -c <prefix of course name, or course alias>`
  * Aggregation over a set of weighted components: `./adv.py -cagg grade1@weight1 ... graden@weightn` where the weights sum to 100
  * Aggregation over a set of courses: `./adv.py -agg entry1 ... entryn` where each entry is either a grade or a grade weighted with credits (e.g. `a2@20`)
  * Conversion from a letter grade to a grade point: `./adv.py -gpa <grade>`
  * Conversion from a grade point to a letter grade: `./adv.py -g <grade point>`
