% bgd, sgd, mbgd on one graph
bgd = importdata('bgd.txt');
sgd = importdata('sgd.txt');
mbgd = importdata('mbgd.txt');
plot(bgd(:,2),bgd(:,1),'b',sgd(:,2),sgd(:,1),'r',mbgd(:,2),mbgd(:,1),'g')
xlabel('number of updates')
ylabel('cost function')
legend('batch gradient descent','stochastic gradient descent','mini batch gradient descent')
% error vs C
errors = importdata('error.txt');
figure()
plot(errors(:,2),errors(:,1))
xlabel('regularization parameter C')
ylabel('percent error on the test data set') 
