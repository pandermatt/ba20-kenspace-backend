import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':
    plt.figure(figsize=(8,10))
    df = pd.read_csv('result.csv')
    boxplot = df.boxplot(column=['Precision','Recall','F-Score'], by='min_df', figsize=(10,4),layout=(1,3), showfliers=False)
    plt.suptitle('')
    # plt.show()
    plt.savefig('temp.pdf', dpi=300)

    # plt.plot(df['N'], df['purity'], label='Purity')
    # plt.plot(df['N'], df['entropy'], label='Entropy')
    # plt.plot(df['N'], df['overall_precision'], label='Precision')
    # plt.plot(df['N'], df['overall_recall'], label='Recall')
    # plt.plot(df['N'], df['F'], label='F Score')
    # plt.title('Cluster Evaluation (top terms per cluster)')
    # # plt.title('Cluster Evaluation (cluster size)')
    # plt.grid(ls = '-.')
    # plt.xlabel("N top terms per cluster")
    # # plt.xlabel("N clusters")
    # plt.legend()
    # # plt.show()
    # plt.savefig('temp.pdf', dpi=300)
