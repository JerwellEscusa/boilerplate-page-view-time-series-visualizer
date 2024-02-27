import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)
df = df.rename(columns={'value': 'views'})

# Clean data
df = df[(df['views'] >= df['views'].quantile(0.025)) & (df['views'] <= df['views'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    df_line = df.copy()
    
    font_labels = {'family': 'sans serif',
                    'color':  'black',
                    'weight': 'normal',
                    'size': 18,
                    }
    plt.style.use('tableau-colorblind10')
    fig, ax = plt.subplots(figsize=(32, 10))
    
    plt.plot(df_line)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=20, fontweight='bold')
    plt.xlabel('Date', fontdict=font_labels)
    plt.ylabel('Page Views', fontdict=font_labels)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Group by year and month, calculate the mean views
    df_bar = df_bar.groupby(['year', 'month']).mean().unstack()
    
    months_legends = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(15, 13))
    
    df_bar.plot.bar(colormap='viridis', ax=ax)
    plt.legend(months_legends, title='Months')
    plt.title('Bar Plots of Monthly Views Grouped by Year')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.xticks(rotation ='horizontal') 

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1, 2, figsize=(20, 10))
    
    sns.boxplot(data=df_box, x='year', y='views', hue='year', palette='cividis', ax=axs[0], legend=False)
    axs[0].set_title('Year-wise Box Plot (Trend)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')
    
    sns.boxplot(data=df_box, x='month', y='views', hue='month', order=month_order, palette='viridis', ax=axs[1])
    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
