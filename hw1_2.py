# -*- coding: utf-8 -*-
"""HW1-2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_-XCcxjkPdxFbRmlT6Q5TKlszIngsbK8
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

# Define the model
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc1 = nn.Linear(28*28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 28*28)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Load and preprocess the MNIST dataset
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)
testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False)

# Train the model and record parameters
def train_and_record(model, trainloader, criterion, optimizer, epochs=10, record_cycle=5):
    model.train()
    layer_params = []
    model_params = []
    for epoch in range(epochs):
        for images, labels in trainloader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        if epoch % record_cycle == 0:
            layer_params.append(model.fc1.weight.data.clone().detach().numpy())
            model_params.append({name: param.clone().detach().numpy() for name, param in model.named_parameters()})
    return layer_params, model_params

# Initialize model, criterion, and optimizer
model = SimpleModel()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Train the model 8 times and record parameters
all_layer_params = []
all_model_params = []
for i in range(8):
    print(f'Training iteration {i+1}...')
    layer_params, model_params = train_and_record(model, trainloader, criterion, optimizer)
    all_layer_params.append(layer_params)
    all_model_params.append(model_params)

def plot_pca(params, title):
    pca = PCA(n_components=2)
    reduced_params = pca.fit_transform(np.array(params).reshape(len(params), -1))
    plt.scatter(reduced_params[:, 0], reduced_params[:, 1])
    plt.title(title)
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.show()

# Plot PCA for layer parameters
for i, layer_params in enumerate(all_layer_params):
    plot_pca(layer_params, f'PCA of Layer Parameters - Training Iteration {i+1}')

# Plot PCA for model parameters
for i, model_params in enumerate(all_model_params):
    flattened_params = [np.concatenate([param.flatten() for param in params.values()]) for params in model_params]
    plot_pca(flattened_params, f'PCA of Model Parameters - Training Iteration {i+1}')

import matplotlib.pyplot as plt

def visualize_gradients_and_loss(model, trainloader, criterion, optimizer, epochs=10):
    model.train()
    gradient_norms = []
    losses = []

    for epoch in range(epochs):
        for images, labels in trainloader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_norm = 0
            for p in model.parameters():
                param_norm = p.grad.data.norm(2)
                total_norm += param_norm.item() ** 2
            total_norm = total_norm ** 0.5
            gradient_norms.append(total_norm)
            losses.append(loss.item())

    # Plot for Gradient Norm
    plt.figure(figsize=(10, 5))
    plt.plot(gradient_norms, label='Gradient Norm', color='b')
    plt.title('Gradient Norm During Training')
    plt.xlabel('Iteration')
    plt.ylabel('Gradient Norm')
    plt.legend()
    plt.show()

    # Plot for Loss
    plt.figure(figsize=(10, 5))
    plt.plot(losses, label='Loss', color='r')
    plt.title('Loss During Training')
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

visualize_gradients_and_loss(model, trainloader, criterion, optimizer)

"""Minimal ratio on a smaller network"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

transform = transforms.Compose([transforms.ToTensor()])
trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=False)

net = Net()
criterion = nn.CrossEntropyLoss()

optimizer = optim.SGD(net.parameters(), lr=0.01)
min_ratios = []
losses = []
for epoch in range(100):
    for i, data in enumerate(trainloader, 0):
        inputs, labels = data
        inputs = inputs.view(-1, 784)
        optimizer.zero_grad()
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        grad_norm = 0
        for param in net.parameters():
            grad_norm += param.grad.norm().item() ** 2
        grad_norm = grad_norm ** 0.5

        # Compute the minimal ratio
        param_norm = 0
        for param in net.parameters():
            param_norm += param.norm().item() ** 2
        param_norm = param_norm ** 0.5
        min_ratio = grad_norm / param_norm

        min_ratios.append(min_ratio)
        losses.append(loss.item())


plt.scatter(min_ratios, losses)
plt.xlabel('Minimal Ratio')
plt.ylabel('Loss')
plt.title('Minimal Ratio vs Loss')
plt.show()





