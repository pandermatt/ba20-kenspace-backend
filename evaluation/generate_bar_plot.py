import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':
    plt.figure(figsize=(8, 4))
    df = pd.read_csv('result.csv')
    # ax = df.plot.line()
    # plt.show()

    # plt.plot(df['N'], df['purity'], label='Purity')
    # plt.plot(df['N'], df['entropy'], label='Entropy')
    plt.plot(df['N'], df['overall_precision'], label='Precision')
    plt.plot(df['N'], df['overall_recall'], label='Recall')
    plt.plot(df['N'], df['F'], label='F Score')
    # plt.title('Cluster Evaluation (top terms per cluster)')
    plt.title('Cluster Evaluation (cluster size)')
    plt.grid(ls = '-.')
    # plt.xlabel("N top terms per cluster")
    plt.xlabel("N clusters")
    plt.legend()
    # plt.show()
    plt.savefig('temp.pdf', dpi=300)
