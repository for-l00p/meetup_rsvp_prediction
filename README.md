***
# Event RSVP Predictor

<i>Flatiron School Data Science Immersive Program</i><br>
<i>Project Date: May 2019 </i>

Predicting yes-RSVP counts for NYC-based events using data sourced from meetup's API and conducting a member segmentation to find groups of similar members in NYC.

***

## Motivation
One of the biggest logistical challenges of event planning is in getting a realistic headcount estimation. Much of event planning is contingent on how many attendees are expected, most importantly choosing on an appropriately-sized venue space.  With the trove of past meetup event data, I thought that there might be a way to predict headcount for an event based on features of the event as well as the group hosting the event.

I started off with regression models and then tried a different approach by framing this into a classification question by creating headcount bins. Because there was a lot of rich information in the event descriptions, I conducted NLP analysis via topic modeling to find latent topics within the events themselves, across all categories. I used those topics as features in the model.

Lastly, I looked at the NYC-based members and clustered similar members based on the interests and groups that they provided on their meetup profiles. The benefit of clustering is that the boundaries generated can be applied to member segmentation for marketing/advertising application.

## Data Cleaning

## Data Exploration

## Modeling

## NLP - Topic Modeling

## Member Clustering

## Takeaways
