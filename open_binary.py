import numpy as np

print("Regression Feature Weights")
print("---")

reg_weights = np.fromfile("regression_weights")

print(reg_weights)
print(np.argsort(reg_weights)[-3:])

print("---")


print("Classification Feature Weights")
print("---")
class_weights = np.fromfile("classification_weights")
print(class_weights)
print(np.argsort(class_weights)[-3:])