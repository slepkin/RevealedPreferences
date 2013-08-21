A Python script that evaluates a given [stable marriage problem instance](http://en.wikipedia.org/wiki/Stable_marriage_problem), uses the [Gale-Shapley algorithm](http://en.wikipedia.org/wiki/Stable_marriage_problem#Solution) to determine its [fully-reduced digraph representation](http://www.jstor.org/discover/10.2307/3109805?uid=3739256&uid=2&uid=4&sid=21102542472061), and prints something to be fed into [Graphviz](http://www.graphviz.org/) to get an image of the digraph.

This requires Python and [Graphviz](http://www.graphviz.org/). Use the command:

```bash
cat sample_input.txt | python one_one_matching.py | neato -T jpeg -Gsplines=true -oOutput
```

This should make an aptly named jpeg that looks pretty.

=========
Last updated 5/14/2013
