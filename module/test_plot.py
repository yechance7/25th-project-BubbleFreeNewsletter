#성능지표 시각화 함수
from sklearn.metrics import confusion_matrix, recall_score, precision_score, f1_score, accuracy_score
import matplotlib.pyplot as plt
import numpy as np


def plot_metrics(conf_matrix, accuracy, precision, recall, f1):
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    # Confusion matrix heatmap
    cax = ax[0].matshow(conf_matrix, cmap='Blues')
    fig.colorbar(cax, ax=ax[0])
    ax[0].set_title('Confusion Matrix')
    ax[0].set_xlabel('Predicted Labels')
    ax[0].set_ylabel('True Labels')

    for (i,j), val in np.ndenumerate(conf_matrix):
        ax[0].text(j,i,f'{val}', ha='center', va='center', color='black')

    # Bar chart for metrics
    metrics = {'Accuracy': accuracy, 'Precision': precision, 'Recall': recall, 'F1 Score': f1}
    ax[1].bar(metrics.keys(), metrics.values(), color=['skyblue', 'orange', 'green', 'red'])
    ax[1].set_ylim([0, 1])
    ax[1].set_title('Evaluation Metrics')

    plt.tight_layout()
    plt.savefig('/root/bub/25th-project-BubbleFreeNewsletter/metrics_plot.png')
    print("Plot saved as 'metrics_plot.png'")

    plt.close()  # Close the plot to free up resources
