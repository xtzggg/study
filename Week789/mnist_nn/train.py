from mnist_loader import load_mnist
from neural_network import NeuralNetwork
import numpy as np

X_train, y_train, X_test, y_test = load_mnist()

nn = NeuralNetwork(input_size=784, hidden_size=100, output_size=10, lr=0.1)
nn.train(X_train, y_train, epochs=5, batch_size=64)

# preds = nn.predict(X_test)
# accuracy = (preds == y_test).mean()
# print(f"Test Accuracy: {accuracy:.4f}")
np.save("weights.npy", {
    "W1": nn.W1, "b1": nn.b1,
    "W2": nn.W2, "b2": nn.b2
})
print("训练完成，权重已保存！")
