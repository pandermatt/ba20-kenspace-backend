import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    plt.figure(figsize=(8, 10))
    df = pd.read_csv('result.csv')
    boxplot = df.boxplot(column=['Precision', 'Recall', 'F-Score'], by='N', figsize=(10, 4), layout=(1, 3),
                         showfliers=False, rot=45)
    plt.suptitle('')
    plt.tight_layout()
    plt.savefig('boxplot.pdf', dpi=300)

    plt.figure(figsize=(8, 10))
    plt.plot(df['N'], df['Purity'], label='Purity')
    plt.plot(df['N'], df['Entropy'], label='Entropy')
    plt.plot(df['N'], df['Precision'], label='Precision')
    plt.plot(df['N'], df['Recall'], label='Recall')
    plt.plot(df['N'], df['F-Score'], label='F Score')
    plt.title('Cluster Evaluation (top terms per cluster)')
    plt.grid(ls='-.')
    plt.xlabel("N top terms per cluster")
    plt.legend()
    plt.savefig('result.pdf', dpi=300)
