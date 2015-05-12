R = importdata('user-shows.txt');
% Do not allocate P and Q to a diagonal matrix to save memory
P = diag(R * R');
Q = diag(R' * R);
% assign S_i, S_u according to part (a)
S_i = diag(Q.^-0.5) * ((R' * R) * diag(Q.^-0.5));
S_u = diag(P.^-0.5) * ((R * R') * diag(P.^-0.5));
% assign user-user and movie-movie collaborative filtering matrices based on part (b)
User_u = S_u * R;
Item_m = R * S_i;
% top 5 similarity scores for Alex using user-user collaborative filtering
tvshows = importdata('shows.txt');
alex_u = User_u(500, 1:100);
alex_u_sorted = sort(alex_u, 'descend');
for i = 1:5
    for j = 1:100
        if alex_u(j) == alex_u_sorted(i)
            X = [tvshows(j),num2str(alex_u_sorted(i))];
            disp(X)
        end
    end
end
% top 5 similarity scores for Alex using movie-movie collaborative filtering
alex_m = Item_m(500, 1:100);
alex_m_sorted = sort(alex_m, 'descend');
for i = 1:5
    for j = 1:100
        if alex_m(j) == alex_m_sorted(i)
            Y = [tvshows(j),num2str(alex_m_sorted(i))];
            disp(Y)
        end
    end
end
% calculate whether the top K-th TV show is watched by Alex in reality
user_alex = importdata('alex.txt');
y_u = zeros(1,19);
y_m = zeros(1,19); 
for k = 1:19
    for i = 1:100
        if alex_u(i) == alex_u_sorted(k)
            y_u(k) = y_u(k) + user_alex(i);
        end
    end 
    for j = 1:100
        if alex_m(j) == alex_m_sorted(k)
            y_m(k) = y_m(k) + user_alex(j);
        end
    end 
end
% calculate true positive rate at top-K
show = 0;
for i = 1:100;
    if user_alex(i) == 1
        show = show + 1;
    end
end
r_u = cumsum(y_u)/show;
r_m = cumsum(y_m)/show;
% plot true positive rate at top-K
x_u = 1:19;
x_m = 1:19;
figure();
plot(x_u, r_u, '--go', x_m, r_m, ':r*');
title('True positive rate at top-K');
xlabel('K');
ylabel('true positive rate');
legend('user-user collaborative filtering', 'movie-movie collaborative filtering');