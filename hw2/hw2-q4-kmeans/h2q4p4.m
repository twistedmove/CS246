data = importdata('data.txt');
cluster = importdata('random20.txt');
secondDocument = data(2,:);
distances = zeros(1,10);
for i = 1:10
    distance = 0;
    for j = 1:58
        distance = distance + (secondDocument(j) - cluster(i,j))^2;
    end
    distances(i) = distance;
end
max = distances(1);
index = 1;
for i = 2:size(distances)
    if distances(i) > max
        max = distances(i);
        index = i;
    end
end
vocab = importdata('vocab.txt');
features = cluster(index,:);
features_sorted = sort(features,'descend');
for i = 1:10
    for j = 1:length(features)
        if features_sorted(i) == features(j)
            disp(vocab(j))
        end
    end
end