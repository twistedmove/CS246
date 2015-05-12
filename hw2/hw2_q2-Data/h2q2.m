X = importdata('HW2_Q2_X.txt');
y = importdata('HW2_Q2_Y.txt');
[U, S, V] = svd(X, 'econ');
r_k = zeros(1,31);
for k = 1:20:601
    w = 0;
    % k columns of U corresponding to the k largest singular values of X
    U_k = U(:,1:k)';
    % calculate simple classifier
    for i = 41:640
        w = w + y(i) * U_k(:,i);
    end
    r = 0;
    % calculate measure of the agreement between the predicted and actual
    % sentiment of the first 40 reviews
    for j = 1:40
        r = r + y(j) * U_k(:,j)' * w;
    end
    r_k((k + 19) / 20) = -r;
end
% plot r in relation to k
k = 1:20:601;
figure();
plot(k, r_k, 'c');
title('how r changes as k varies');
xlabel('k');
ylabel('r');