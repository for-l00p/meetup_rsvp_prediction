***
# Event RSVP Predictor

Predicting yes-RSVP counts for NYC-based events using data sourced from Meetup's API.

## Motivation

[Meetup](https://www.meetup.com/) is one of first and most popular event-based social networking sites. With humble beginnings in New York City, the Meetup community now stretches all around the world. The founders of Meetup realized the importance of building real communities through in-person interactions in the form of community events.

One of the biggest challenges of event planning is getting a realistic headcount estimation. Almost all of the logistical details of event planning are contingent on how many attendees are expected - most importantly, choosing on an appropriately-sized venue space.  With the trove of past meetup event data, I thought that there might be a way to predict headcount for an event based on features of the event as well as the group hosting the event.

Additionally, because there was a lot of rich information in the event descriptions, I conducted NLP analysis via topic modeling to find latent topics within the event descriptions across all categories.

## Data Cleaning

My final dataset included contained 8,624 NYC-based groups and 25,424 events (covering September-October 2018).

Before conducting initial analyses, I reviewed the raw data to address missing values by removing a column altogether or filling with a value.

<p align="center">
 <img width="400" alt="datacleaning" height="400" src="images/datacleaning.png">
</p>

<p align="center">
 <img width="500" alt="datacleaning_groups" height="350" src="images/datacleaning_groups.png">
</p>


## Data Exploration

#### Events

As expected, most events were located in the greater New York City area but interestingly, events were also organized across the country and abroad. (Note the events shown in the maps below are from a sample of just 2,000 events.)

<p align='center'>
 <img width="400" alt="nycevents" height="225" src="images/nyc_events_map.png">

 <img width="400" alt="globevents" height="225" src="images/glob_events_map.png">

</p>

The number of events held by each group varied across the category of the hosting group. For example, book-club groups held much fewer events than singles groups. This intuitively makes sense - book clubs generally need to space out meetings to ensure members have enough time to read sections of a book whereas the singles group look to provide as many 'mingling' opportunities as possible.

<p align='center'>
 <img width="800" alt="events" height="700" src="images/events_eda.png">

</p>


#### Target

The yes-RSVP count for events ranged from 0 to 592 with an average of 13 and a median of 4. There were a small number of outliers -  283 events with 0 yes-RSVPs and 351 events with yes-RSVPs greater than 100. The total number of outliers in the dataset amounted to just a small portion so I retained all values since such a small value would have a negligible effect on the model prediction.

<p align='center'>
 <img width="600" alt="target" height="400" src="images/target_info.png">
</p>


#### Groups



## Modeling

Below is a summary of all the regression models I ran. We'll take a closer look at the baseline and the best performing models below.



#### Baseline


#### Best Model


#### Feature Importance


## (NLP) Topic Modeling of Event Descriptions


## Takeaways

One of the biggest caveats for this model is that 'yes' RSVP count inherently is not an accurate reflection of actual event attendance. However, until accurate and comprehensive attendance data is available, the yes-RSVP count can serve as a suitable proxy. When and if actual attendance data is available, the same preprocessing and modeling steps can be taken as outlined here to obtain predictions using real attendance data.

## Next Steps

For next steps, I plan to gather event data for the rest of 2018 to improve model performance. Additionally, I would like to frame this question as a classification problem to provide a range prediction instead of a single-value. Providing a lower and upper headcount will likely be much easier for event organizers to work with.



- reg w/ all data
- class w/ all data (measure performance w/ ROC-AUC graphs, confusion matrices & precision/recall/F1)
    - SMOTE (post train/test/split to avoid data leakage)
    - under-sample majority class
    - note that you do not have to have a perfect 1:1 ratio across all classes - try any ratio that is better than what you currently have
- visualize centroids of member-clusters?
