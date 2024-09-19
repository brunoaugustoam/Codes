import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def wind_rose_diagram(wind_direction,web=False):

       bin_edges = np.arange(-5, 366, 10) #Força a separacao 0,360 para os bins
       number_of_strikes, bin_edges = np.histogram(wind_direction, bin_edges) #pega a contagem de ocorrencias do vento dentro da direção especificada
       number_of_strikes[0] += number_of_strikes[-1] #soma à primeira direcao, -5 a 5 o ultimo intervalo, de 355 a 365, which is the same
       fig = plt.figure(figsize=(16,8))

       ax = fig.add_subplot(122, projection='polar')

       ax.bar(np.deg2rad(np.arange(0, 360, 10)), number_of_strikes[:-1], 
       width=np.deg2rad(10), bottom=0.0, color='.8', edgecolor='k')
       ax.set_theta_zero_location('N')
       ax.set_theta_direction(-1)
       ax.set_thetagrids(np.arange(0, 360, 10), labels=np.arange(0, 360, 10))
       ax.set_rgrids(np.arange(0, number_of_strikes[:-1].max() + 10, ((number_of_strikes[:-1].max() // 5 )//10 + 1)*10), angle=0, weight= 'black')
       #    ax.set_title(f'Rose Diagram of Wind Direction', y=1.10, fontsize=12)

       if web:
              return fig
       else:
              plt.show()    


def wind_speed_density(wind_direction,wind_speed,web=False):
    fig = plt.figure(figsize=(18,8))

    # To plot a regular Stereogram of wind, uncomment below 
    ax = fig.add_subplot(111, projection='stereonet')
    ax.density_contourf(wind_direction-90, wind_speed, measurement='poles', cmap='Reds')
    ax.grid()

    if web:
            return fig
    else:
            plt.show()  

          

def get_pairplot(df, columns,hue='SEASON',palette= {'WINTER': 'C0', 'SPRING': 'C2', 'SUMMER': 'r', 'FALL': 'C1'}):
    return sns.pairplot(df[columns], hue=hue, palette=palette, markers=["o", "^", "H","D"], plot_kws={'alpha': 0.6})


def plot_wind_hist(wind_direction, wind_speed,web=False):
    fig, ax = plt.subplots(1,2,figsize=(8,5) ,)
    bin_edges = np.arange(-5, 366, 10)
    ax[0].hist(wind_direction, bins=bin_edges, color='grey', alpha=0.7)

    ax[0].set_ylabel('Frequency')
    ax[0].set_xlabel('DirMaxGust')
    mu = np.round(np.mean(wind_direction),1)
    md = np.round(np.median(wind_direction),1)
    std = np.round(np.std(wind_direction),1)
    m = np.round(stats.mode(wind_direction),1)[0].item()
    ax[0].title.set_text(f'Mode: {m}, Mean: {mu}, Median: {md}, Std: {std}')

    bin_edges = np.arange( wind_speed.min(), wind_speed.max(), 2)
    ax[1].hist(wind_speed, bins=bin_edges, color='lightgrey', alpha=0.7)
    ax[1].set_ylabel('Frequency')
    ax[1].set_xlabel('SpdMaxGust (Km/h)')
    mu = np.round(np.mean(wind_speed),1)
    md = np.round(np.median(wind_speed),1)
    std = np.round(np.std(wind_speed),1)
    m = np.round(stats.mode(wind_speed),1)[0].item()
    ax[1].title.set_text(f'Mode: {m}, Mean: {mu}, Median: {md}, Std: {std}')

    if web:
        return fig
    else:
        plt.show()

def plot_precipitation(df,col='TOTAL_PRECIPITATION',web=False):
    fig,ax = plt.subplots(1,1, figsize=(8,5))

    x = df[col]
    bin_edges = np.arange( x.min(), x.max(), 5)
    ax.hist(x,bins=bin_edges)
    ax.set_ylabel('Frequency')
    ax.set_xlabel('TOTAL_PRECIPITATION')
    ax.set_xlim(df['TOTAL_PRECIPITATION'].min(), df['TOTAL_PRECIPITATION'].max())
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Total Precipitation (mm)')
    if web:
        return fig
    else:
        plt.show()


def plot_humidity(df,col=[ 'MIN_REL_HUMIDITY','MAX_REL_HUMIDITY'],web=False):
    fig,ax = plt.subplots(1,len(col), figsize=(8,5), sharey=True)

    for (i,temp) in enumerate(col):
        
        x = df[temp]
        bin_edges = np.arange( x.min(), x.max(), 5)
        ax[i].hist(x,bins=bin_edges)
        ax[0].set_ylabel('Frequency')
        ax[i].set_xlabel(col[i])
        ax[i].set_xlim(df['MIN_REL_HUMIDITY'].min(), df['MAX_REL_HUMIDITY'].max())
        ax[i].set_ylabel('Frequency')
        ax[i].set_xlabel(f'{col[i]}')
    if web:
        return fig
    else:
        plt.show()

# import plotly.figure_factory as ff
def plot_temperature(dataframe, temperature=['MIN_TEMPERATURE','MEAN_TEMPERATURE', 'MAX_TEMPERATURE'], web=False):
    #fig, ax = plt.subplots(1, len(temperature), figsize=(8, 5), sharey=True)
    df = dataframe.copy()
    # for (i, temp) in enumerate(temperature):
    #     x = df[temp]
    #     bin_edges = np.arange(x.min(), x.max(), 5)
    #     # Histogram with color mapping
    #     ax[i].hist(x, bins=bin_edges, color='orange', alpha=0.7)

    #     ax[0].set_ylabel('Frequency')
    #     ax[i].set_xlabel(f'{temp}')
    #     ax[i].set_title(f'{temp}')  # Add informative title
    #     ax[i].set_xlim(df['MIN_TEMPERATURE'].min(), df['MAX_TEMPERATURE'].max())

    # bin_edges = np.arange(x.min(), x.max(), 5)
    colors=['blue','green', 'red']
    fig, ax = plt.subplots(1, figsize=(8, 5), sharey=True)
    bin_edges = np.arange(int(df['MIN_TEMPERATURE'].min()-1), int(df['MAX_TEMPERATURE'].max()+1), 5)
    for (i, temp) in enumerate(temperature):
        
        # Histogram with color mapping
        ax.hist(df[temp], bins=bin_edges, color=colors[i], alpha=0.4, label=temperature[i])

        ax.set_ylabel('Frequency')
        ax.set_xlabel(f'Temperature')
        ax.set_xlim(int(df['MIN_TEMPERATURE'].min()-1), int(df['MAX_TEMPERATURE'].max()+1))
    plt.legend()


    # Group data together
    # 
    # df.dropna(inplace=True)
    # hist_data = [df[f'{i}'] for i in temperature]# df['MIN_TEMPERATURE'], df['MAX_TEMPERATURE']]

    # group_labels = ['MEAN_TEMPERATURE', 'MIN_TEMPERATURE', 'MAX_TEMPERATURE']

    # # Create distplot with custom bin_size
    # fig = ff.create_distplot(
    #         hist_data, group_labels, bin_size=[5, 5, 5])


    if web:
        return fig
    else:
        plt.show()