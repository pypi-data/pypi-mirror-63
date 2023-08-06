This package contains functionality useful for econometric work with panel data.
Its name, originally standing for "high-dimensional fixed effects," is now misleading.

Useful features are
* Groupby: A class allowing for fast operations similar to Pandas groupby-apply and groupby-transform
functionality, but performing significantly faster with user-written functions. See
documentation [here](http://esantorella.com/2016/06/16/groupby/).
* find_collinear_cols and remove_collinear_cols: Functions
for dealing with multicollinearity which operate quickly on CSC matrices.
* make_lags: Makes within-group lags (frequently useful with panel data)

You can install hdfe through pip: "pip install hdfe"
