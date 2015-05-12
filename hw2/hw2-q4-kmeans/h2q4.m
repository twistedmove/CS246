% plot cost function
C1 = importdata('costFunctionC1.txt');
C2 = importdata('costFunctionC2.txt');
figure();
y_1 = C1(4601:4601:92020);
y_2 = C2(4601:4601:92020);
(C1(4601) - C1(46010))/C1(4601)
(C2(4601) - C2(46010))/C2(4601)
x_1 = 1:20;
x_2 = 1:20;
plot(x_1, y_1, '--go', x_2, y_2, ':r*');
title('cost function in relation the number of iterations');
xlabel('i');
ylabel('¦Õ(i)');
legend('c1.txt', 'c2.txt');