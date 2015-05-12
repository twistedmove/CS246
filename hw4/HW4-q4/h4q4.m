% scatter plot
errors = importdata('error.txt');
x = errors(:,2);
y = errors(:,1);
scatter(x,y)
set(gca,'xscale','log')
set(gca,'yscale','log')
m = -10:0;
n = -4:8;
set(gca,'xtick',power(10,m))
set(gca,'ytick',power(10,n))
xlabel('word frequency')
ylabel('relative error')
title('scatter plot of relative error as a function of word frequency')