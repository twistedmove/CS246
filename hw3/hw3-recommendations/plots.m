Efunction = importdata('ratings.error.txt');
x = 1:40;
plot(x,Efunction)
xlabel('number of iterations')
ylabel('objective function E')

Efunction = importdata('ratings.newerror.txt');
x = 1:40;
plot(x,Efunction)
xlabel('number of iterations')
ylabel('objective function E')

lambda2 = importdata('largerlambda.txt');
lambda0 = importdata('smallerlambda.txt');
k = 1:10;
plot(k, lambda2(1:10,1), k, lambda0(1:10,1))
xlabel('k')
ylabel('training error')
legend('lambda = 0.2', 'lambda = 0')
plot(k, lambda2(1:10,2), k, lambda0(1:10,2))
xlabel('k')
ylabel('test error')
legend('lambda = 0.2', 'lambda = 0')

newlambda2 = importdata('newlargerlambda.txt');
newlambda0 = importdata('newsmallerlambda.txt');
k = 1:10;
plot(k, newlambda2(1:10,1), k, newlambda0(1:10,1))
xlabel('k')
ylabel('training error')
legend('lambda = 0.2', 'lambda = 0')
plot(k, newlambda2(1:10,2), k, newlambda0(1:10,2))
xlabel('k')
ylabel('test error')
legend('lambda = 0.2', 'lambda = 0')
