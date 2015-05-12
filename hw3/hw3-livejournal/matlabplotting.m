% part i
iteration = importdata('q4c1.txt');
actual = [7 5 4 3];
epsilon = [0.1 0.5 1 2];
theoretical = log(499923)./log(1+epsilon);
figure();
plot(epsilon, actual, epsilon, theoretical)
xlabel('epsilon')
ylabel('number of iterations')
legend('actual','theoretical')
% part ii
graph = importdata('q4c2.txt');
number = graph(:,1);
rho = graph(:,2);
E = graph(:,3);
S = graph(:,4);
figure();
plot(number, rho)
xlabel('iteration')
ylabel('rho(S)')
figure();
plot(number, E)
xlabel('iteration')
ylabel('|E(S)|')
figure();
plot(number, S)
xlabel('iteration')
ylabel('|S|')
% part iii
community = importdata('q4c3.txt');
dense = 1:20;
rhoc = community(:,1);
Ec = community(:,2);
Sc = community(:,3);
figure();
plot(dense, rhoc)
xlabel('community')
ylabel('rho(S)')
figure();
plot(dense, Ec)
xlabel('community')
ylabel('|E(S)|')
figure();
plot(dense, Sc)
xlabel('community')
ylabel('|S|')
