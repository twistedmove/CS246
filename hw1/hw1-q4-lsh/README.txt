This directory contains an simple implementation of Locality-Sensitive
Hashing (LSH) algorithm by Indyk et al. The main functions are (see
documentation in each file for more details):

*** lsh.m - creates the LSH data structure for a given data set.

*** lshprep.m, lshfunc.m - these functions, respectively, set up the LSH
hashing functions and the hash tables based on these functions. You
may not need to call these directly (they are called inside lsh.m)

*** lshins.m - insert data into the LSH data structure. Again, usually you
may not need this function since it, too, is called inside lsh.m, but
you will need it if you need to insert additional data points after
the hash tables are created.

*** lshlookup.m - the approximate similarity search using the LSH. 

*** lshstats.m - examine statistics of LSH data structure

Note: If you are using an earlier version of MATLAB than 7.4, then before 
using any of the above code, you need to copy the files (downloaded from 
http://www.mathworks.com/matlabcentral/fileexchange/18685)included in the
bsx subdirectory and paste them into the same directory as the above files, 
and then:
- from the MATLAB command line run: mex -setup 
- choose the c compiler available on your machine (e.g., Lcc)
- and finally run: mex bsxarg.c



Included is also a dataset:

*** patches.mat - sample of 59500 20x20 greylevel image patches

*********************************

For a simple example, we will use the data in patches.mat:
59500 20x20 patches, reshaped into 400-dimensional column vectors,
taken from a bunch of motorcycle images. 


>> load patches;

build 20 hash tables, using 24-bit keys, under the simple LSH scheme,
and index the patches array:

>> T1=lsh('lsh',20,24,size(patches,1),patches,'range',255);

You should see, for each hash table, something like this:

 B UNLIMITED 24 bits 20 tables
13390 distinct buckets
Table 1 adding 13390 buckets (now 13390)
Table 1: 59500 elements
10940 distinct buckets
Table 2 adding 10940 buckets (now 10940)
Table 2: 59500 elements
...


(note: the insertion process may take a while...)

This means that the data (to remind you, 59,500 examples) were hashed
into 13,390 buckets in this table. That is good, since it *probably*
means that the distribution of examples into buckets is reasonable,
i.e. most of the buckets contain just a few examples.  What you want
to avoid is the case when the number of buckets is very low, i.e., 200
buckets here would mean that there are, necessarily, some huge
buckets, and at search time those would cancel the efficiency effect
of LSH. If that happens, you probably need to increase the number of
bits in the hash keys (try increasing just by a few, say, from 20 to
25).

The number of hash tables is another parameter to play with. For
example, in this case we can probably decrease it to, say, 10, and
still get good results. Mostly, this is a matter of empirical
performance testing, with the data at hand.

The line:

Table 1: 59500 elements

indicates that the number of distinct examples indexed by this table
is 59,500 (in this case, this means that all the original examples are
indexed in this table). This will always be the case if bucket
capacity is unlimited (B=inf). 

However, if you specify a finite B (see lsh.m), this number may be
somewhat lower than the number of examples; if that happens, this
means that some of the buckets would have more than B examples hashed
into them. This often means trouble (see above about large buckets),
and can be resolved by increasing the number of bits.

You can review the statistics of an LSH data structure in more detail by calling
>> lshstats(T1);
20 tables, 24 bits
Table 1: 59500 in 13390 bkts, med 1, max 2229, avg 518.46
Table 2: 59500 in 10940 bkts, med 1, max 4205, avg 863.20
Table 3: 59500 in 13533 bkts, med 1, max 2435, avg 485.97

This means that, e.g., table 1 has 
* 13,390 buckets, 
* median occupancy is 1 example per bucket, 
* maximum occupancy is 2,229 examples,
* expected occupancy of a bucket is 518.46. Expectation is taken
with respect to a randomly drawn point; thus, with a single huge
bucket, there is a large probability that a point would fall into that
bucket, and thus it contributes a lot to the expected occupancy; this
is not the same as taking the mean of bucket occupancy!

We can analyze the tables in a bit more detail:
>> lshstats(T1,100);
20 tables, 24 bits
Table 1: 59500 in 13390 bkts, med 1, max 2229, avg 518.46, 56 (27607)> 100
Table 2: 59500 in 10940 bkts, med 1, max 4205, avg 863.20, 55 (29437)> 100
Table 3: 59500 in 13533 bkts, med 1, max 2435, avg 485.97, 55 (26600)> 100
Table 4: 59500 in 15199 bkts, med 1, max 6185, avg 997.58, 50 (25616)> 100
Table 5: 59500 in 13089 bkts, med 1, max 2900, avg 486.65, 68 (27759)> 100
Table 6: 59500 in 16312 bkts, med 1, max 6212, avg 997.58, 51 (24616)> 100
Table 7: 59500 in 14974 bkts, med 1, max 2797, avg 565.61, 47 (25827)> 100
Table 8: 59500 in 13302 bkts, med 1, max 2875, avg 566.96, 61 (28507)> 100
Table 9: 59500 in 13649 bkts, med 1, max 3276, avg 705.35, 43 (26762)> 100
Table 10: 59500 in 15024 bkts, med 1, max 2460, avg 518.14, 49 (25488)> 100
Table 11: 59500 in 12071 bkts, med 1, max 3450, avg 647.23, 56 (29121)> 100
Table 12: 59500 in 12821 bkts, med 1, max 2331, avg 533.25, 62 (27829)> 100
Table 13: 59500 in 12717 bkts, med 1, max 3410, avg 595.69, 56 (28003)> 100
Table 14: 59500 in 13822 bkts, med 1, max 3622, avg 581.17, 58 (26503)> 100
Table 15: 59500 in 13647 bkts, med 1, max 4846, avg 819.41, 57 (27857)> 100
Table 16: 59500 in 11779 bkts, med 1, max 1815, avg 470.46, 61 (28286)> 100
Table 17: 59500 in 13478 bkts, med 1, max 4224, avg 695.39, 54 (28806)> 100
Table 18: 59500 in 14067 bkts, med 1, max 2607, avg 543.24, 55 (26250)> 100
Table 19: 59500 in 11399 bkts, med 1, max 4317, avg 844.15, 51 (29223)> 100
Table 20: 59500 in 14701 bkts, med 1, max 3060, avg 555.39, 56 (27413)> 100


This, in addition to the information explained above, tells us that in
Talbe 1, there are 56 buckets with more than 100 elements, holding the
total of 27,607 elements - possibly not good news, since this means
that the distribution of data into buckets may not be very uniform
after all: more than half the data are stuck in relatively few large
buckets. This is likely a consequence of some structure in the data
(i.e., the data themselves are not uniform). The main practical
implication of this is, again, potential increase in time it takes to
look up data in the table. 

One way to address this is, again, to increase k; another way could be to
tell lshlookup to not exhaustively look at all the elements in the
matching bucket (see below). 

Before we do that, we can run an even more detailed diagnostic: test
the performance of the tables on a data set. Below we do that by
running lookup on the first 1000 patches, and asking for at least two NN
(since the reference data contains the same patches, we know that
there is always at least one NN).

>> lshstats(T1,'test',patches,patches(:,1:1000),2);
20 tables, 24 bits
Table 1: 59500 in 13390 bkts, med 1, max 2229, avg 518.46
...
Total 59500 elements
  Running test...10% 20% 30% 40% 50% 60% 70% 80% 90% 100% 
  # of comparisons: mean 2554.16, max 9779, failures: 4

So, on average we look at > 2,500  examples for each lookup - about
4.3%. That's not very good. On the other hand, we have almost no failures.

We could rebuild the LSH structure with more bits, but first we will
try something else: reduce the number of tables.

>> lshstats(T1(1:5),'test',patches,patches(:,1:1000),2);
...
  Running test...10% 20% 30% 40% 50% 60% 70% 80% 90% 100% 
  # of comparisons: mean 1457.84, max 7699, failures: 53

This shows a typical tradeoff: we now have about 2.5% comparison rate,
but about 5% lookup. failure rate. Going to a few more tables:

>> lshstats(T1(1:10),'test',patches,patches(:,1:1000),2);
...
  Running test...10% 20% 30% 40% 50% 60% 70% 80% 90% 100% 
  # of comparisons: mean 1956.60, max 9074, failures: 13

This seems fairly good. Now let's try to increase k:


>> T2=lsh('lsh',20,50,size(patches,1),patches,'range',255);

>> lshstats(T2,'test',patches,patches(:,1:1000),2);
...
  Running test...10% 20% 30% 40% 50% 60% 70% 80% 90% 100% 
  # of comparisons: mean 622.79, max 5376, failures: 366

The number of comparisons is much better, but the number of failures
is too high. We can try adding tables:

>> T2(21:40) = lsh('lsh',20,50,size(patches,1),patches,'range',255);
>> lshstats(T2,'test',patches,patches(:,1:1000),2);
...
  Running test...10% 20% 30% 40% 50% 60% 70% 80% 90% 100% 
  # of comparisons: mean 925.35, max 6197, failures: 312

Doesn't help much. We could try to increase L further; however, for
now we will just stick with L=10, k=24.

We will now investigate the quality of the lookup. Let the 50-th patch
be the test sample:

>> figure(1);imagesc(reshape(patches(:,50),20,20));colormap gray;axis image

We can search the LSH data structure for the 11 nearest neighbors under the
L1 norm. (we mean 10-NN, but the first one will, of course, be the
50-th patch itself, and we want to find 10 real neighbors):

>> tic; [nnlsh,numcand]=lshlookup(patches(:,50),patches,T2,'k',11,'distfun','lpnorm','distargs',{1});toc
Elapsed time is 0.042590 seconds.


Show the 10-NN:

>> figure(2);clf;
>> for k=1:10, subplot(2,5,k);imagesc(reshape(patches(:,nnlsh(k+1)),20,20)); colormap gray;axis image; end

You can now also do the exhaustive search, and compare the results:
>> tic;d=sum(abs(bsxfun(@minus,patches(:,50),patches)));
[ignore,ind]=sort(d);toc;
Elapsed time is 0.449682 seconds.

>> figure(3);clf;
>> for k=1:10, subplot(2,5,k);imagesc(reshape(patches(:,ind(k+1)),20,20));colormap gray;axis image; end

You should see, among the 10-NN, many of the same examples, although
not necessarily exactly the same, since LSH provides only an approximate search
method. If the results of LSH are significantly inferior to those of
the exact brute-force search, something went wrong along the way.

**************************

We can do the same for the e2lsh scheme:

>> Te=lsh('e2lsh',50,30,size(patches,1),patches,'range',255,'w',-4);

I.e., use 30 projections per function, aiming to divide each projection into 4
intervals (see comments in lshfunc.m).

>> lshstats(Te,'test',patches,patches(:,1:1000),2);
...
  Running test...10% 20% 30% 40% 50% 60% 70% 80% 90% 100% 
  # of comparisons: mean 2294.09, max 11596, failures: 12 


Note: using L2, we can say


>> tic; [nnlsh,numcand]=lshlookup(patches(:,50),patches,Te,'k',11,'distfun','lpnorm','distargs',{2});toc
>> tic;d=sqrt(sum(bsxfun(@minus,patches(:,50),patches).^2)); [ignore,ind]=sort(d);toc;

Note that in this case, neighbors returned by LSH are exactly the same
as the true 10-NN (of course, it is not guaranteed to happen for any
query and any number of neighbors.)

