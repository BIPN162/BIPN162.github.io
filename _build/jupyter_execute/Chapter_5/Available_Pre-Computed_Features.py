#!/usr/bin/env python
# coding: utf-8

# # Available Pre-Computed Features

# The Allen Institute also has many more precomputed features. Many of them give access to more information on the electrophysiology, morphology, and metadata on the cells available in the Allen. We will demonstrate some of these features below.

# In[1]:


#Import all the necessary packages and initalize an instance of the cache
import pandas as pd
from allensdk.core.cell_types_cache import CellTypesCache
from allensdk.api.queries.cell_types_api import CellTypesApi
import matplotlib.pyplot as plt
ctc = CellTypesCache(manifest_file='cell_types/manifest.json')


# The `all_features` method can be used to access the morphology and electrophysiology of all the cells in the database and merges the two into a single table. This method can take into two optional inputs; `dataframe` and `require_reconstructon`.

# In[2]:


all_features = ctc.get_all_features(dataframe = True)
all_features.head()


# Since we set the `dataframe` parameter to `True`, the method returns our data as a nice and neat pandas dataframe. If set to `False`, the method returns a dictionary. We can all check to make sure all the columns are there by executing the `get_ephys_features` and `get_morphology_features` seperately and comparing the columns.

# In[3]:


all_features_columns = all_features.columns
all_features_columns


# In[4]:


# Store all ephys columns in a variable 
ephys_df = pd.DataFrame(ctc.get_ephys_features()).set_index('specimen_id')
ephys_columns = ephys_df.columns

# Store all morphology columns in a variable 
morphology_df = pd.DataFrame(ctc.get_morphology_features()).set_index('specimen_id')
morphology_columns = morphology_df.columns 

# Combine the two into one list
ephys_and_morphology = list(morphology_columns) + list(ephys_columns)

# Sort and Compare the columns to make sure they are all there 
print(list(all_features_columns).sort() == ephys_and_morphology.sort())


# By default, `get_all_features()` only returns ephys and morphology features for cells that have reconstructions. To access all cells regardless of reconstruction, set the parameter `require_recontruction` to `False`.

# Below we have created a pandas dataframe from the data on mouse cells and set the row indices to be the `id` column. This will give us the metadata on mouse cells along and ID's to choose from. 

# In[5]:


mouse_df = pd.DataFrame(ctc.get_cells(species = [CellTypesApi.MOUSE])).set_index('id')
mouse_df.head()


# The Allen has many pre-computed features that you might consider comparing across cells. Some of these features include input resistance (input_resistance_mohm), Adapation ratio (adaptation), Average ISI (avg_isi), and many others (you can find a complete glossary <a href = "https://docs.google.com/document/d/1YGLwkMTebwrXd_1E817LFbztMjSTCWh83Mlp3_3ZMEo/edit#heading=h.t0p3wngfkxc1"> here </a>).

# We combined the human metadata with our electrophysiology dataframe. From our new human electrophysiology dataframe, we created two dataframes to compare spiny dendrite types to aspiny dendrite types.

# In[6]:


# gather all spiny and aspiny e cells into different dataframes
mouse_spiny_df = mouse_ephys_df[mouse_ephys_df['dendrite_type']=='spiny']
mouse_aspiny_df = mouse_ephys_df[mouse_ephys_df['dendrite_type']=='aspiny']


# In[44]:


# plot our figure 
plt.boxplot([mouse_spiny_df['input_resistance_mohm'], mouse_aspiny_df['input_resistance_mohm']])
plt.ylabel('Input Resistance (mohm)')
plt.xticks([1,2], ['Spiny', 'Aspiny'])
plt.title('Input Resistance of Mouse Spiny vs Aspiny Neuron Dendrite Types')

plt.show()


# In[45]:


# download our Human cells data and combine with our electrophysiology data
human_df = pd.DataFrame(ctc.get_cells(species = [CellTypesApi.HUMAN])).set_index('id')
human_ephys_df = human_df.join(ephys_df)


# In[46]:


# compare two different brain structures 
human_MTG_df = human_ephys_df[human_ephys_df['structure_area_abbrev']=='MTG']
human_MFG_df = human_ephys_df[human_ephys_df['structure_area_abbrev']=='MFG']


# In[47]:


# plot our figure 
plt.boxplot([human_MTG_df['tau'], human_MFG_df['tau']])
plt.ylabel('tau')
plt.xticks([1,2], ['MTG', 'MFG'])
plt.title('Tau of MTG Cells vs MFG Cells')

plt.show()


# In[48]:


# drop all null values in our column of interest in order to plot
human_MTG_df = human_MTG_df.dropna(subset =['avg_isi'])
human_MFG_df = human_MFG_df.dropna(subset = ['avg_isi'])


# In[49]:


# plot our figure 
plt.boxplot([human_MTG_df['avg_isi'], human_MFG_df['avg_isi']])
plt.ylabel('Mean value of all interspike intervals in a sweep')
plt.xticks([1,2], ['MTG', 'MFG'])
plt.title('Average ISI of MTG Cells vs MFG Cells')

plt.show()


# In[50]:


# plot our figure 
plt.boxplot([human_ephys_df['trough_v_short_square'], mouse_ephys_df['trough_v_short_square']])
plt.ylabel('Voltage of after-hyperpolarization')
plt.xticks([1,2], ['Human', 'Mouse'])
plt.title('Voltage of after-hyperpolarization of Human Cells vs Mouse Cells')

plt.show()


# In[51]:


# compare cells of different disease states 
human_tumor_df = human_ephys_df[human_ephys_df['disease_state']=='tumor']
human_epilepsy_df = human_ephys_df[human_ephys_df['disease_state']=='epilepsy']

# remove all NaN values in adaptation column to create boxplot 
human_tumor_df = human_tumor_df.dropna(subset = ['adaptation'])
human_epilepsy_df = human_epilepsy_df.dropna(subset = ['adaptation'])


# In[52]:


# plot our figure 
plt.boxplot([human_tumor_df['adaptation'], human_epilepsy_df['adaptation']])
plt.ylabel('rate at which firing speeds up or slows down during a stimulus')
plt.xticks([1,2], ['Tumor', 'Epilepsy'])
plt.title('Adaptation of Tumor Cells vs Epilepsy Cells')

plt.show()


# In[ ]:




