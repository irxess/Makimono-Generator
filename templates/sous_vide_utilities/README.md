This folder contains some utilites for sous vide cooking.

First and foremost, there is a time estimator, which is based on the timing estimations in The Modernist Cuisine (1st ed, volume 2, page 276-279).
Because simple multivariate regressions in spreadsheets did not work,
and sklearn in python yielded horrible fits for all the multiple regression and other ml models I figured out how to trhow at the problem,
I made a custom prediction algorithm around kd-trees, and treating sample estimate points as vertices in a 3-d shape laying out a surface in the temperature dimention.
From here, it's a simple "find last component of vector given the plane it should be in" lookup.
Because it beat out sklearn for my data, and I had to do some shaping and scrubbing of the data for it to work well,
we'll call it "advanced graphics based machine learning".

To use the estimator you have to include it, and the KD-trees in your page.
You should end up with something like:

```html
<head>
...
<script src="k-d_tree-spherical.js" ></script>
<script src="k-d_tree-slab.js" ></script>
<script src="k-d_tree-sausage.js" ></script>
<script src="k-d_tree-hamburger.js" ></script>
<script src="k-d_tree-time_estimator.js" ></script>
...
</head>
```

Note that the `k-d_tree-creator.js` file is not used.
This is because the raw data files are comparable in size to the generated k-d trees,
so there is no need to waste compute at the users end when the work of creating the trees has already been done while figuring out how to make them and test that they work well enough.

After you've loaded the trees and `k-d_tree-time_estimator.js`, you should be able to get an estimate by calling the `EstimateTimeNeeded()` function like this:

```js
EstimateTimeNeeded(45, 72, "spherical"));
```

It should yield results like "39 minutes 42 seconds".

For more descriptions on how to use, see the user-facing page once it is done, for more technical details read the scripts themselves.
