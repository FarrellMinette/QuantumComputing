import pennylane as qml
from pennylane import numpy as np

dev = qml.device("lightning.qubit", wires=1)

@qml.qnode(dev, interface="autograd")
def circuit(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=0)
    return qml.expval(qml.PauliZ(0))

def cost(x):
    return circuit(x)

opt = qml.GradientDescentOptimizer(stepsize=0.4)
params = np.array([0.051, 0.027], requires_grad=True)

while(cost(params)!=-1.000):
    params = opt.step(cost, params)

print('Optimized rotation angles: \n', params)
print('Cost: \n', cost(params))