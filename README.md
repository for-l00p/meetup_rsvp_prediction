***
# Event RSVP Predictor

Predicting yes-RSVP counts for NYC-based events using data sourced from [Meetup's](https://www.meetup.com/) API.

## Motivation

Meetup is one of the most popular event-based social networking sites out there. With humble beginnings in New York City, the Meetup community now stretches all around the world 16 years later. The founders of Meetup realized believed in the importance of building real communities through in-person contact.

One of the biggest challenges of event planning is getting a realistic headcount estimation. Almost all of the logistical details of event planning are contingent on how many attendees are expected - most importantly, choosing on an appropriately-sized venue space.  With the trove of past meetup event data, I thought that there might be a way to predict headcount for an event based on features of the event as well as the group hosting the event.

Additionally, because there was a lot of rich information in the event descriptions, I conducted NLP analysis via topic modeling to find latent topics within the events themselves, across all categories. I replaced the group_category feature (tech, socializing, etc.) with the event topic since the ```group_category``` did not score highly on the feature importance graph derived from the first iteration of the xbgoost model that included ```group_category``` as a feature.

## Data Cleaning
There were null values to address in the events and groups dataset. Based on the percentage of null values for a given feature, the feature column was either dropped or filled with an imputed value.

<p align="center">
 <img width="400" alt="datacleaning" height="400" src="datacleaning.png">
</p>

<p align="center">
 <img width="500" alt="datacleaning_groups" height="350" src="datacleaning_groups.png">
</p>


## Data Exploration

I created a function to make GET requests to the events and groups API endpoint to collect data.

#### Events

As expected, most events were located in the greater New York City area but interestingly, events were also organized across the country and abroad.

[insert local and global map images side by side]

The number of events held by each group varied across the category of the hosting group. For example, groups within the 'book club' category held much fewer events than groups within the 'singles' category. This intuitively makes sense - book clubs generally need to space out meetings to ensure members have enough time to read a certain portion of a book; members of singles groups are highly interested in mingling so they are interested in going to as many events as possible with other like-minded individuals.)


#### Groups


## Modeling

I performed a number of different regression models on the dataset. Below are the results of the regression model using ```group_category``` followed by a new iteration of the model that replaces the category with ```event_topic```.


## NLP: Topic Modeling of Event Descriptions


## Takeaways & Next Steps

One of the biggest caveats for this model is that 'yes' RSVP count inherently is not an accurate reflection of actual event attendance. However, until actually attendance data is collected, we

- reg w/ all data
- class w/ all data (measure performance w/ ROC-AUC graphs, confusion matrices & precision/recall/F1)
    - SMOTE (post train/test/split to avoid data leakage)
    - under-sample majority class
    - note that you do not have to have a perfect 1:1 ratio across all classes - try any ratio that is better than what you currently have
- visualize centroids of member-clusters?
