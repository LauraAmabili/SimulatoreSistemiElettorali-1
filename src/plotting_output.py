import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

def draw_output(final_output) :

    raw_data = {'NomeLista': df_final_distribution['Eleggibile'], 
        'Votes': df_final_distribution['Votes'],
        'Seats': df_final_distribution['Seats']}
    
    df = pd.DataFrame(raw_data, columns = ['NomeLista', 'Votes', 'Seats'])
    #df['Total_Votes'] = df['Votes'].sum()

    plt.figure(figsize=(16,8))
    # plot chart
    ax1 = plt.subplot(121, aspect='equal')
    #plt.pie(data['Votes'], labels=df['NomeLista'], autopct='%.2f')
    df.plot(kind='pie', y = 'Votes', ax=ax1, autopct='%1.2f%%', 
     startangle=90, shadow=False, labels=df['NomeLista'], legend = False, fontsize=14)

    # plot table
    ax2 = plt.subplot(122)
    plt.axis('off')
    tbl = table(ax2, df, loc='center')
    tbl.auto_set_font_size(True)
    tbl.set_fontsize(14)
    plt.show()

    return 0