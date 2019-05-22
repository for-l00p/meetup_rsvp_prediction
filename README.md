***
# Event RSVP Predictor

Predicting yes-RSVP counts for NYC-based events using data sourced from meetup's API.

## Motivation
One of the biggest logistical challenges of event planning is in getting a realistic headcount estimation. Almost all of the logistical details of event planning are contingent on how many attendees are expected - most importantly, choosing on an appropriately-sized venue space.  With the trove of past meetup event data, I thought that there might be a way to predict headcount for an event based on features of the event as well as the group hosting the event.

I started off with regression models and then tried a different approach by framing this into a classification question by creating headcount bins. I initially had events covering 2 months (September and October) and when plotting the distribution of headcount for those months, there was a clear class imbalance issues. One tactic to address that was to gather more data on events for the entire year.





 Because there was a lot of rich information in the event descriptions, I conducted NLP analysis via topic modeling to find latent topics within the events themselves, across all categories. I replaced the group_category feature (tech, socializing, etc.) with the event topic since the group_category did not score highly on the feature importance graph derived from the xbgoost model.

## Data Cleaning
There were null values to address in the events and groups dataset:

<p align="center">
 <img width="400" alt="datacleaning" height="400" src="datacleaning.png">
</p>

<p align="center">
 <img width="800" alt="datacleaning_groups" height="350" src="datacleaning_groups.png">
</p>


## Data Exploration




## Modeling

### Regression Models


### Classification Models


## NLP: Topic Modeling of Event Descriptions

## Takeaways & Next Steps
