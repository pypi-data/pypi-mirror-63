import pandas as pd

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import IPython
import plotly
import plotly.graph_objs as go
# from utils import configure_plotly_browser_state

class GraphUtils:
    """
    Contains graph utility methods
    """
    def __init__(self, prev_release: str, curr_release: str, prev_release_version=220, curr_release_version=222):
        """
        Init code
        """
        self.last_release = prev_release
        self.this_release = curr_release
        self.last_release_version = prev_release_version
        self.this_release_version = curr_release_version
        
        self.objects_to_colors = {
            'Account': '#6C76cf',
            'Case': '#EEC74A',
            'CollaborationGroup': '#6589EE',
            'Contact': '#8E7DE8',
            'Lead': '#F47450',
            'Opportunity': '#FAAB4a',
            'User': '#2EB1C2'
        }

        self.sobjects = ['Account', 'Contact', 'Case', 'CollaborationGroup', 'Lead', 'Opportunity', 'User']

        self.appversion_colors = {
          str(self.last_release):'#7c868dff', 
          str(self.this_release):'#00a1e0ff'
        }

        self.release_version_colors = {prev_release_version:'#7c868dff', curr_release_version:'#00a1e0ff'}

        self.network_colors = {
          'Wifi': '#aa000044',
          'LTE': '#00aa0044',
          '3G': '#0000aa44'
        }  

    def visualize_using_boxplot(self, obj_: object, numcols: int,release_criteria: int, ylimit=None):
      v = [str(self.last_release), str(self.this_release)] # `v` is a sorted (older -> newer) list of app Versions.
      p = {self.last_release:'#7c868dff', self.this_release:'#00a1e0ff'}
      if (numcols == 1): 
        import seaborn as sns
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(nrows=1, ncols=numcols, figsize=(10,12), sharey=True)
        ax.plot(np.linspace(-20,120,1000), [release_criteria]*1000, 'r') 
        sns.boxplot(x="appVersion", y="EPT", hue="appVersion", data=obj_, order=v, palette=p)
        plt.show()
      else:
        import seaborn as sns
        import matplotlib.pyplot as plt
        fig, [ax1, ax2] = plt.subplots(nrows=1, ncols=numcols, figsize=(24,12), sharey=True)

        ax1.plot(np.linspace(-20,120,1000), [release_criteria]*1000, 'r')  
        ax2.plot(np.linspace(-20,120,1000), [release_criteria]*1000, 'r')

        sns.boxplot(ax=ax1, x="entitytype", y="EPT", data=obj_[obj_['appVersion']==self.last_release], order=self.objects_to_colors.keys(), palette=self.objects_to_colors.values())
        sns.boxplot(ax=ax2, x="entitytype", y="EPT", data=obj_[obj_['appVersion']==self.this_release], order=self.objects_to_colors.keys(), palette=self.objects_to_colors.values())
        plt.ylim(0,None)
        ax1.set_title(str(self.last_release) + ' - Wifi')
        ax2.set_title(str(self.this_release) + ' - Wifi')
        plt.show()
      
      sns.despine(offset=10, trim=True)

    def visualize_using_boxplot_releaseVersion(self, obj_: object, numcols: int ,release_criteria: int, ylimit:int):
      v = [220, 222] # `v` is a sorted (older -> newer) list of app Versions.
    #   p = ['#00a1e0ff', '#7c868dff']#, '#00b2a9ff', '#963cbdff']
      p = {220:'#7c868dff', 222:'#00a1e0ff'}
      if (numcols == 1): 
        import seaborn as sns
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(nrows=1, ncols=numcols, figsize=(10,12), sharey=True)
        sns.boxplot(x="releaseVersion", y="EPT", hue="releaseVersion", data=obj_, order=v, palette=p)
        ax.plot(np.linspace(-20,120,1000), [release_criteria]*1000, 'r') 
        plt.show()
      else:
        import seaborn as sns
        import matplotlib.pyplot as plt
        fig, [ax1, ax2] = plt.subplots(nrows=1, ncols=numcols, figsize=(24,12), sharey=True)
        
    #     print(obj_[obj_['appVersion']==last_release].head)
        sns.boxplot(ax=ax1, x="entitytype", y="EPT", data=obj_[obj_['releaseVersion']==self.last_release_version], order=self.objects_to_colors.keys(), palette=self.objects_to_colors.values())
        sns.boxplot(ax=ax2, x="entitytype", y="EPT", data=obj_[obj_['releaseVersion']==self.this_release_version], order=self.objects_to_colors.keys(), palette=self.objects_to_colors.values())
        plt.ylim(0,None)
        ax1.set_title(str(self.last_release_version) + ' - Wifi')
        ax2.set_title(str(self.this_release_version) + ' - Wifi')
        ax1.plot(np.linspace(-20,120,1000), [release_criteria]*1000, 'r')  
        ax2.plot(np.linspace(-20,120,1000), [release_criteria]*1000, 'r')
        plt.show()
        
       
      sns.despine(offset=10, trim=True)

    # Violin Function 
    def visualize_using_voilinplot(self, obj: object, numcols: int ,release_criteria: int):
      try:
        if (numcols == 1): 
          fig, ax = plt.subplots(nrows=1, ncols=numcols, figsize=(250,12), sharey=True)
          sns.violinplot(y="EPT",x="appVersion", hue="appVersion", data=obj, order=v, palette=p)
          ax.plot(np.linspace(-20,120,1000), [release_criteria]*1000, 'r')
        else:
          import matplotlib.pyplot as plt
          fig, [ax1, ax2] = plt.subplots(nrows=1, ncols=numcols, figsize=(24,12), sharey=True)

          sns.violinplot(ax=ax1, y="EPT", x="entitytype", data=obj[obj['appVersion']==last_release], order=objects_to_colors.keys(), palette=objects_to_colors.values())
          sns.violinplot(ax=ax2, y="EPT", x="entitytype", data=obj[obj['appVersion']==this_release], order=objects_to_colors.keys(), palette=objects_to_colors.values())

          plt.ylim(0,None)
          ax1.set_title(str(self.last_release) + ' - Wifi')
          ax2.set_title(str(self.this_release) + ' - Wifi')
          ax1.plot(np.linspace(-20,120,1000), [release_criteria]*1000, 'r')  # Draw a horizontal line at y=release_criteria for the P95 goal
          ax2.plot(np.linspace(-20,120,1000), [release_criteria]*1000, 'r')  # Draw a horizontal line at y=release_criteria for the P95 goal
        sns.despine(offset=10, trim=True)
      except Exception as e:
        print("visualize_using_voilinplot():: Error plotting data: ", e)
      

    #Entity Based Distribution Plots
    def cmp_aura_flexipage(self, obj, xaxislimit: int):
      try:
        if 'entitytype' in obj.columns:
          fig, ax = plt.subplots(nrows=len(self.sobjects), ncols=1, figsize=(12,14), sharex=True)
          for i, sobj in enumerate(self.sobjects):
            for appversion in [self.last_release, self.this_release]:
              d =  obj[(obj['entitytype'] == sobj) & (obj['appVersion'] == appversion)]['EPT']
              sns.kdeplot(d, color=self.appversion_colors[appversion], ax=ax[i], shade=True, label=appversion)
              ax[i].set(yticks=[])
              ax[i].set_xlabel('')
              ax[i].set_ylabel(sobj)
              plt.xlim(0,xaxislimit)
              sns.despine(ax=ax[i], bottom=True, left=True)
          fig.subplots_adjust(hspace=.25)
        else:
          fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,8))
          sns.distplot(obj[obj['appVersion']==self.this_release]['EPT'], ax=ax, label=str(self.this_release), color=self.appversion_colors[self.this_release])
          sns.distplot(obj[obj['appVersion']==self.last_release]['EPT'], ax=ax, label=str(self.last_release), color=self.appversion_colors[self.last_release])
          plt.legend()
          ax.set_title('EPT')
        plt.show()
      except Exception as e:
        print("cmp_aura_flexipage():: Error plotting data: ", e)

    def cmp_aura_flexipage_release_version(self, obj, xaxislimit: int):
      try:
        if 'entitytype' in obj.columns:
          fig, ax = plt.subplots(nrows=len(self.sobjects), ncols=1, figsize=(12,14), sharex=True)
          for i, sobj in enumerate(self.sobjects):
            for release_version in [self.last_release_version, self.this_release_version]:
              d =  obj[(obj['entitytype'] == sobj) & (obj['releaseVersion'] == release_version)]['EPT']
              sns.kdeplot(d, color=self.release_version_colors[release_version], ax=ax[i], shade=True, label=release_version)
              ax[i].set(yticks=[])
              ax[i].set_xlabel('')
              ax[i].set_ylabel(sobj)
              plt.xlim(0,xaxislimit)
              sns.despine(ax=ax[i], bottom=True, left=True)
          fig.subplots_adjust(hspace=.25)
        else:
          fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,8))
          sns.distplot(obj[obj['releaseVersion']==self.this_release_version]['EPT'], ax=ax, label=str(self.this_release_version), color=self.release_version_colors[self.this_release_version])
          sns.distplot(obj[obj['releaseVersion']==self.last_release_version]['EPT'], ax=ax, label=str(self.last_release_version), color=self.release_version_colors[self.last_release_version])
          plt.legend()
          ax.set_title('EPT')
        plt.show()
      except Exception as e:
        print("cmp_aura_flexipage():: Error plotting data: ", e)

    #Entity Based Network EPT Distribution Plots
    def cmp_network(self, obj, xaxislimit: int):
      try:
        fig, ax = plt.subplots(nrows=len(self.sobjects), ncols=1, figsize=(12,16), sharex=True)
        for i, sobj in enumerate(self.sobjects):
          for network in ['Wifi', 'LTE', '3G']:
            d =  obj[(obj['entitytype'] == sobj) & (obj['network'] == network)]['EPT']
            sns.kdeplot(d, color=self.network_colors[network], ax=ax[i], shade=True, label=network)
            ax[i].set(yticks=[])
            ax[i].set_xlabel('')
            ax[i].set_ylabel(sobj)
            plt.xlim(0,xaxislimit)
            sns.despine(ax=ax[i], bottom=True, left=True)
        
        fig.subplots_adjust(hspace=.25)
      except Exception as e:
        print("cmp_network():: Error ploting data: ", e)

    def mem_analysis(self, object_raw, aggregate_function, split_by_sobjects=True):
      self.configure_plotly_browser_state()
      plotly.offline.init_notebook_mode(connected=False)

      figure_list = []

      if split_by_sobjects and 'entitytype' in object_raw.columns:
        for sobj in self.sobjects:
          entity_raw = object_raw[object_raw["entitytype"]==sobj]
          object_data_wifi = entity_raw.groupby(['appVersion']).apply(aggregate_function)
          object_data1 = object_data_wifi[object_data_wifi.index == self.last_release]
          object_data2 = object_data_wifi[object_data_wifi.index == self.this_release]

          object_subset1 = object_data1[['P25', 'P50', 'P75', 'P95']]
          object_tuples1 = [tuple(x) for x in object_subset1.values]

          object_subset2 = object_data2[['P25', 'P50', 'P75', 'P95']]
          object_tuples2 = [tuple(x) for x in object_subset2.values]

          if not object_tuples1 or not object_tuples2:
            print("not enough data for " + sobj)
            continue

          s = [str(self.last_release), str(self.this_release)]
          object_trace1 = go.Bar(
              x=['P25', 'P50', 'P75', 'P95'],
              y=[object_tuples1[0][0], object_tuples1[0][1], object_tuples1[0][2], object_tuples1[0][3]],
              name=s[0],
              marker=dict(
                  color='rgb(255, 153, 0)',
              )
          )
          object_trace2 = go.Bar(
              x=['P25', 'P50', 'P75', 'P95'],
              y=[object_tuples2[0][0], object_tuples2[0][1], object_tuples2[0][2], object_tuples2[0][3]],
              name=s[1],
              marker=dict(
                  color='rgb(49,130,189)'
              )
          )

          object_data = [object_trace1, object_trace2]
          object_layout = go.Layout(
              title='Memory Utilization for {sobj} across releases'.format(sobj=sobj),
              xaxis=dict(
                  title='Percentile',
                  tickfont=dict(
                      size=14,
                      color='rgb(107, 107, 107)'
                  ),
                  tickangle=-45),
              barmode='group',
              yaxis=dict(
                  title='Memory Utilized (mb)',
                  titlefont=dict(
                      size=16,
                      color='rgb(107, 107, 107)'
                  ),
                  tickfont=dict(
                      size=14,
                      color='rgb(107, 107, 107)'
                  )
              )
          )

          object_fig = go.Figure(data=object_data, layout=object_layout)
          plotly.offline.iplot(object_fig)
          figure_list.append(object_fig)
      else:
        object_data_wifi = object_raw.groupby(['appVersion']).apply(aggregate_function)
        object_data1 = object_data_wifi[object_data_wifi.index == self.last_release]
        object_data2 = object_data_wifi[object_data_wifi.index == self.this_release]

        object_subset1 = object_data1[['P25', 'P50', 'P75', 'P95']]
        object_tuples1 = [tuple(x) for x in object_subset1.values]

        object_subset2 = object_data2[['P25', 'P50', 'P75', 'P95']]
        object_tuples2 = [tuple(x) for x in object_subset2.values]

        s = [str(self.last_release), str(self.this_release)]
        object_trace1 = go.Bar(
            x=['P25', 'P50', 'P75', 'P95'],
            y=[object_tuples1[0][0], object_tuples1[0][1], object_tuples1[0][2], object_tuples1[0][3]],
            name=s[0],
            marker=dict(
                color='rgb(255, 153, 0)',
            )
        )
        object_trace2 = go.Bar(
            x=['P25', 'P50', 'P75', 'P95'],
            y=[object_tuples2[0][0], object_tuples2[0][1], object_tuples2[0][2], object_tuples2[0][3]],
            name=s[1],
            marker=dict(
                color='rgb(49,130,189)'
            )
        )

        object_data = [object_trace1, object_trace2]
        object_layout = go.Layout(
            title='Memory Utilization across releases',
            xaxis=dict(
                title='Percentile',
                tickfont=dict(
                    size=14,
                    color='rgb(107, 107, 107)'
                ),
                tickangle=-45),
            barmode='group',
            yaxis=dict(
                title='Memory Utilized (mb)',
                titlefont=dict(
                    size=16,
                    color='rgb(107, 107, 107)'
                ),
                tickfont=dict(
                    size=14,
                    color='rgb(107, 107, 107)'
                )
            )
        )
        object_fig = go.Figure(data=object_data, layout=object_layout)
        plotly.offline.iplot(object_fig)
        figure_list.append(object_fig)
      # return figure_list

    def configure_plotly_browser_state(self):
      display(IPython.core.display.HTML('''
            <script src="/static/components/requirejs/require.js"></script>
            <script>
              requirejs.config({
                paths: {
                  base: '/static/base',
                  plotly: 'https://cdn.plot.ly/plotly-1.5.1.min.js?noext',
                },
              });
            </script>
            '''))

