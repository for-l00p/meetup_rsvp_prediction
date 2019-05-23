***
# Event RSVP Predictor

Predicting yes-RSVP counts for NYC-based events using data sourced from meetup's API.

## Motivation
One of the biggest logistical challenges of event planning is in getting a realistic headcount estimation. Almost all of the logistical details of event planning are contingent on how many attendees are expected - most importantly, choosing on an appropriately-sized venue space.  With the trove of past meetup event data, I thought that there might be a way to predict headcount for an event based on features of the event as well as the group hosting the event.

 Because there was a lot of rich information in the event descriptions, I conducted NLP analysis via topic modeling to find latent topics within the events themselves, across all categories. I replaced the group_category feature (tech, socializing, etc.) with the event topic since the ```group_category``` did not score highly on the feature importance graph derived from the first iteration of the xbgoost model that included ```group_category``` as a feature.

## Data Cleaning
There were null values to address in the events and groups dataset. Based on the percentage of null values for a given feature, the feature column was either dropped or filled with an imputed value.

<p align="center">
 <img width="400" alt="datacleaning" height="400" src="datacleaning.png">
</p>

<p align="center">
 <img width="800" alt="datacleaning_groups" height="350" src="datacleaning_groups.png">
</p>


## Data Exploration

I pulled down events for NYC-based groups for the months of September and October and explored the contents in this dataset.

#### Events

As expected, most of the events were located in Manhattan and its immediate vicinities (Queens, Brooklyn, New Jersey) but interestingly, there were events held across the country and internationally as well.

[insert local and global map images side by side]

The number of events held by each group varied across the category of the hosting group. For example, the 'book club' category of groups 


#### Groups

## Modeling


### Regression Models


## NLP: Topic Modeling of Event Descriptions

## Takeaways & Next Steps

One of the biggest caveats for this model is that 'yes' RSVP counts inherently are not an accurate reflection of actual event attendance. However, until better

- reg w/ all data
- class w/ all data (measure performance w/ ROC-AUC graphs, confusion matrices & precision/recall/F1)
    - try SMOTE
    - try undersampling majority class
    - note that you do not have to have a perfect 1:1 ratio across all classes - try any ratio that is better than what you currently have
- visualize centroids of member-clusters?
