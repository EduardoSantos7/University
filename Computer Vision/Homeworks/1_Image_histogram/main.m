grayImage = imread('im.png'); % Read the original image and store it in a matrix 'grayImage'
[pixelCount, grayLevels] = imhist(grayImage); % 'pixelCount' represents the length of the color map
max_value = max(max(grayImage)); % Get the absolute max
min_value = min(min(grayImage)); % Get the absolute min
max_pixelcount = max(pixelCount);
min_pixelcount = min(pixelCount);
[~, x] = max(pixelCount); % Find the gray level at which the largest amount of pixels are.
[~, y] = min(pixelCount); % Find the gray level at which the least amount of pixels are.
level_with_max = grayLevels(x);
level_with_min = grayLevels(y);

figure
subplot(1, 2, 1);
imshow(grayImage); % Show the original image
subplot(1, 2, 2);
bar(pixelCount); % Display the bars of the Histogram
grid on;
title('Histogram of Original Image', 'FontSize', 12);
xlabel('gray levels')
ylabel('frequency')