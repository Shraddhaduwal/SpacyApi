import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

sns.set(style="darkgrid")


def visualize(name):
    path = "Results" + "/" + name
    df = pd.read_csv(path)
    col_1 = df.columns[1]  # for frequency
    col_2 = df.columns[0]  # for name of anything like noun, adj

    sns.barplot(x=col_1, y=col_2, data=df)
    plt.title(f'{col_2} {col_1}')
    plt.tight_layout()
    # plt.show()

    # Saving figures into a bytes-object and exposing it whenever req through flask
    bytes_image = io.BytesIO(b"f'{col_1}_{col_2}.csv'")
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image
