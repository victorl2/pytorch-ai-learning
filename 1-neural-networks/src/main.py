import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
from torchvision import transforms, datasets

####
# Based on Sentdex videos: https://www.youtube.com/watch?v=i2yPxY2rOzs, https://www.youtube.com/watch?v=ixathu7U-LQ
####

img_size = 28
flatten_img_size = img_size * img_size


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(flatten_img_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 10)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        return F.log_softmax(self.fc4(x), dim=1)


if __name__ == '__main__':
    print("### Hello, this is a example using the built-in dataset from pytorch vision ###\n")

    print("Downloading training dataset")
    train = datasets.MNIST("", train=True, download=True,
                           transform=transforms.Compose([transforms.ToTensor()]))

    print("Downloading validation dataset")
    test = datasets.MNIST("", train=False, download=True,
                          transform=transforms.Compose([transforms.ToTensor()]))

    trainset = torch.utils.data.DataLoader(train, batch_size=10, shuffle=True)
    testset = torch.utils.data.DataLoader(test, batch_size=10, shuffle=True)

    total = 0
    counter_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for data in trainset:
        Xs, ys = data
        for y in ys:
            counter_dict[int(y)] += 1
            total += 1

    # This is how you would plot a image from the training dataset
    # plt.imshow(data[0][0].view(28,28))
    # plt.show()

    print("\nPercentage for each number in training samples:")
    for i in counter_dict:
        print(f"{i}: {(counter_dict[i]/total*100):.2f}%")

    print("\n####Now the fun begins - lets create the neural network")

    print("Creating a instance of the neural network")
    net = Net()
    print(net)

    print("\nGenerating a random 28x28 image")
    X = torch.rand((img_size, img_size))
    X = X.view(-1, flatten_img_size)

    print("passing the image to the network and checking the output")
    output = net(X)
    print(output)

    optmizer = optim.Adam(net.parameters(), lr=0.001)

    EPOCHS = 4

    for epoch in range(EPOCHS):
        for data in trainset:
            X, y = data # Batch of images and batch of results describing what number each image is
            net.zero_grad() # Make the gradient zero, only the currect batch will influence the currenct adjust of weights
            output = net(X.view(-1,flatten_img_size)) # Pass the batch of images to the network
            loss = F.nll_loss(output, y) # Calculate the loss. aka how wrong the neural network is at the moment
            loss.backward() # backpropagate the in all the layers of the neural network
            optmizer.step()
        print(loss)


    correct = 0
    total = 0

    # Calculating the accuracy of neural network without computing gradients
    with torch.no_grad():
        for data in trainset:
            X, y = data # Batch of images and batch of results describing what number each image is
            output = net(X.view(-1,flatten_img_size)) # Pass the batch of images to the network
            for idx, i in enumerate(output): 
                if torch.argmax(i) == y[idx]: # Checking if the prediction is the currect number in the y vector
                    correct += 1
                total +=1
    
    print("Accuracy:", round(correct/total, 3))

    plt.imshow(X[0].view(img_size,img_size))
    plt.show()

    print(torch.argmax(net(X[0].view(-1,flatten_img_size))[0]))