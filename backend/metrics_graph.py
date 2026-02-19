import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc

def plot_classification_metrics(y_true, y_pred, y_prob):
    """
    Calculates and plots various performance metrics for a classification model.

    Args:
        y_true: True labels.
        y_pred: Predicted labels.
        y_prob: Predicted probabilities for the positive class.
    """

    # 1. Print Classification Report
    print("--- Classification Report ---")
    print(classification_report(y_true, y_pred))
    print("-" * 30)


    # 2. Plot Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Negative', 'Positive'],
                yticklabels=['Negative', 'Positive'])
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')
    plt.show()


    # 3. Plot ROC Curve
    fpr, tpr, thresholds = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()

def plot_accuracy_and_loss(history):
    """
    Plots training & validation accuracy and loss values from a training history.

    Args:
        history (dict): A dictionary containing 'accuracy', 'val_accuracy',
                        'loss', and 'val_loss' lists.
    """
    # Plot accuracy
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history['accuracy'], label='Train Accuracy')
    plt.plot(history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(loc='upper left')

    # Plot loss
    plt.subplot(1, 2, 2)
    plt.plot(history['loss'], label='Train Loss')
    plt.plot(history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(loc='upper right')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # --- Example Usage ---

    print("--- Running Example 1: Classification Metrics ---")
    # Example data for a binary classification problem
    y_true = np.array([0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0])
    y_pred = np.array([0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0])
    # Probabilities for the positive class (class 1)
    y_prob = np.array([0.1, 0.9, 0.3, 0.2, 0.8, 0.4, 0.1, 0.7, 0.4, 0.95, 0.2, 0.6, 0.85, 0.15])

    plot_classification_metrics(y_true, y_pred, y_prob)


    print("\n--- Running Example 2: Accuracy and Loss Graphs ---")
    # Example history data (e.g., from a Keras model.fit() call)
    # Each list represents the metric value at the end of each epoch.
    history = {
        'accuracy': [0.60, 0.65, 0.71, 0.76, 0.80, 0.82, 0.85, 0.87, 0.88, 0.90],
        'val_accuracy': [0.58, 0.63, 0.69, 0.73, 0.77, 0.79, 0.81, 0.83, 0.84, 0.85],
        'loss': [1.1, 0.95, 0.80, 0.65, 0.55, 0.50, 0.45, 0.40, 0.38, 0.35],
        'val_loss': ['1.2', '1.05', '0.90', '0.78', '0.68', '0.62', '0.58', '0.53', '0.51', '0.49']
    }

    plot_accuracy_and_loss(history)