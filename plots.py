import matplotlib.pyplot as plt

# Define the recall and precision values
recall = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
precision = [0.8130, 0.6832, 0.6115, 0.5739, 0.5071, 0.4562, 0.4025, 0.3546, 0.3060, 0.2479, 0.1642]

# Create the plot
plt.plot(recall, precision, marker='.')
plt.title('Precision-Recall EN RUN-2')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.grid(True)
plt.show()
