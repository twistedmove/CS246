load patches;
% build 10 hash tables, using 24-bit keys, under the simple LSH scheme,
% and index the patches array
T1 = lsh('lsh',10,24,size(patches,1),patches,'range',255);
lshtotal = 0;
lineartotal = 0;

for i = 100:100:1000
    tic;
    % search the LSH data structure for the 3 nearest neighbors under the
    % L1 norm.
    [nnlsh,numcand] = lshlookup(patches(:,i),patches,T1,'k',4,'distfun','lpnorm','distargs',{1});
    toc;
    % ensure lshlookup returns at least 4 values
    while length(nnlsh) < 4
        tic;
        T1 = lsh('lsh',10,24,size(patches,1),patches,'range',255);
        [nnlsh,numcand] = lshlookup(patches(:,i),patches,T1,'k',4,'distfun','lpnorm','distargs',{1});
        toc;
    end
    lshtotal = lshtotal + toc;
    tic;
    % do exhaustive linear search
    d=sum(abs(bsxfun(@minus,patches(:,i),patches)));
    [ignore,ind]=sort(d);
    index = ind(1:4);
    toc;
    lineartotal = lineartotal + toc;
end
% calculate the average time for LSH search and linear search
lshaverage = lshtotal / 10
linearaverage = lineartotal / 10

k = 24;
Y1 = zeros(1,6);
truedistance = zeros(1,10);
for L = 10:2:20
    T2=lsh('lsh',L,k,size(patches,1),patches,'range',255);
    error = 0;
    for i = 100:100:1000
        [nnlsh,numcand] = lshlookup(patches(:,i),patches,T2,'k',4,'distfun','lpnorm','distargs',{1});
        % ensure lshlookup returns at least 4 values
        while length(nnlsh) < 4
            T2 = lsh('lsh',10,24,size(patches,1),patches,'range',255);
            [nnlsh,numcand] = lshlookup(patches(:,i),patches,T2,'k',4,'distfun','lpnorm','distargs',{1});
        end
        % do exhaustive linear search for 10 times     
        d=sum(abs(bsxfun(@minus,patches(:,i),patches)));
        [ignore,ind]=sort(d);
        index = ind(1:4);
        truedistance(i/100) = norm(patches(:, i)-patches(:, index(2)), 1)+norm(patches(:, i)-patches(:, index(3)), 1)+norm(patches(:, i)-patches(:, index(4)), 1);
        % calculate the sum of the 1-norm of the vector of the euclidian
        % distance between nearest neighbours
        lshdistance = norm(patches(:, i)-patches(:, nnlsh(2)), 1)+norm(patches(:, i)-patches(:, nnlsh(3)), 1)+norm(patches(:, i)-patches(:, nnlsh(4)), 1);
        error = error + 0.1 * lshdistance / truedistance(i/100);
    end
    Y1((L-8)/2) = error;
end
% plot the error value as a function of L
figure();
X1 = 10:2:20;
plot(X1, Y1);

L = 10;
Y2 = zeros(1,5);
truedistance = zeros(1,10);
for k = 16:2:24
    T3=lsh('lsh',L,k,size(patches,1),patches,'range',255);
    error = 0;
    for i = 100:100:1000
        [nnlsh,numcand] = lshlookup(patches(:,i),patches,T3,'k',4,'distfun','lpnorm','distargs',{1});
        % ensure lshlookup returns at least 4 values
        while length(nnlsh) < 4
            T3 = lsh('lsh',10,24,size(patches,1),patches,'range',255);
            [nnlsh,numcand] = lshlookup(patches(:,i),patches,T3,'k',4,'distfun','lpnorm','distargs',{1});
        end
        % do exhaustive linear search for 10 times      
        d=sum(abs(bsxfun(@minus,patches(:,i),patches)));
        [ignore,ind]=sort(d);
        index = ind(1:4);
        % calculate the sum of the 1-norm of the vector of the euclidian
        % distance between true nearest neighbours
        truedistance(i/100) = norm(patches(:, i)-patches(:, index(2)), 1)+norm(patches(:, i)-patches(:, index(3)), 1)+norm(patches(:, i)-patches(:, index(4)), 1);
        % calculate the sum of the 1-norm of the vector of the euclidian
        % distance between LSH nearest neighbours
        lshdistance = norm(patches(:, i)-patches(:, nnlsh(2)), 1)+norm(patches(:, i)-patches(:, nnlsh(3)), 1)+norm(patches(:, i)-patches(:, nnlsh(4)), 1);
        error = error + 0.1 * lshdistance / truedistance(i/100);
    end
    Y2((k-14)/2) = error;
end
% plot the error value as a function of k
figure();
X2 = 16:2:24;
plot(X2, Y2);

i = 100;
N = 11;
T4=lsh('lsh',10,24,size(patches,1),patches,'range',255);
[nnlsh,numcand] = lshlookup(patches(:,i),patches,T4,'k',N,'distfun','lpnorm','distargs',{1});
% ensure lshlookup returns at least N values
while length(nnlsh) < N
    T4 = lsh('lsh',10,24,size(patches,1),patches,'range',255);
    [nnlsh,numcand] = lshlookup(patches(:,i),patches,T4,'k',N,'distfun','lpnorm','distargs',{1});
end
d=sum(abs(bsxfun(@minus,patches(:,i),patches)));
[ignore,ind]=sort(d);
index = ind(1:11);
% plot 10 nearest neighbours found by LSH method
figure();
for k = 1:10
    subplot(2, 5, k);
    imagesc(reshape(patches(:, nnlsh(k + 1)), 20, 20));
    colormap gray;
    axis equal;
    axis square;
    axis tight;
end
% plot 10 nearest neighbours found by linear search method
figure();
for k = 1:10
    subplot(2, 5, k);
    imagesc(reshape(patches(:, index(k + 1)), 20, 20));
    colormap gray;
    axis equal;
    axis square;
    axis tight;
end
% plot the image patch itself
figure();
imagesc(reshape(patches(:, i), 20, 20));
colormap gray;
axis equal;
axis square;
axis tight;
