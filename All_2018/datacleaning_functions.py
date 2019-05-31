# Helper functions for cleaning all 2018 events data
from meetup_api_functions import get_subway_distances
import pandas as pd
import pickle


def load_events():
    """
    This function loads all monthly events, then merges into one variable
    and returns the data in a dataframe.
    --INPUT--
    None
    --OUPUT--
    Dataframe
    """
    with open('monthly_events_2018/sepoct_events.pkl', 'rb') as f:
        sepoct_events = pickle.load(f)

    with open('monthly_events_2018/nov_events.pkl', 'rb') as f:
        nov_events = pickle.load(f)

    with open('monthly_events_2018/jan_events.pkl', 'rb') as f:
        jan_events = pickle.load(f)

    with open('monthly_events_2018/feb_events.pkl', 'rb') as f:
        feb_events = pickle.load(f)

    with open('monthly_events_2018/mar_events.pkl', 'rb') as f:
        mar_events = pickle.load(f)

    with open('monthly_events_2018/apr_events.pkl', 'rb') as f:
        apr_events = pickle.load(f)

    with open('monthly_events_2018/may_events.pkl', 'rb') as f:
        may_events = pickle.load(f)

    with open('monthly_events_2018/jun_events.pkl', 'rb') as f:
        jun_events = pickle.load(f)

    with open('monthly_events_2018/jul_events.pkl', 'rb') as f:
        jul_events = pickle.load(f)

    with open('monthly_events_2018/aug_events.pkl', 'rb') as f:
        aug_events = pickle.load(f)

    with open('monthly_events_2018/dec_events.pkl', 'rb') as f:
        dec_events = pickle.load(f)

    raw_2018 = sepoct_events+nov_events+jan_events+feb_events+mar_events + \
        apr_events+may_events+jun_events+jul_events+aug_events+dec_events

    return pd.DataFrame(raw_2018)


def clean_events(dataframe):
    """
    This function will perform all data cleaning activities.
    --INPUT--
    Dataframe
    --OUTPUT--
    Dataframe
    """
    new_df = dataframe

    # convert values in duration column from milliseconds to minutes
    new_df['duration'] = new_df['duration'].apply(lambda x: x/60000)

    # label encode value for whether group's join-mode is open or not
    new_df['group_is_open'] = new_df.group.apply(lambda x: 1 if x['join_mode'] == 'open' else 0)

    # extract group_id from the group column which contains a dictionary of group details
    new_df['group_id'] = new_df.group.apply(lambda x: x.get('id'))

    # rename column to note time unit of the data
    new_df.rename(columns={'duration': 'duration_min'}, inplace=True)

    # fill in NaNs, then label encode
    new_df['how_to_find_us'].fillna(0, inplace=True)
    new_df['has_how_to_find'] = new_df['how_to_find_us'].apply(lambda x: 1 if x != 0 else 0)

    new_df['rsvp_limit'].fillna(0, inplace=True)
    new_df['has_rsvp_limit'] = new_df['rsvp_limit'].apply(lambda x: 1 if x != 0 else 0)

    # fill in Nans, then clean text using regex helper function
    new_df.description.fillna(value='None', inplace=True)
    new_df['description'] = new_df['description'].apply(lambda x: clean_text(x))

    # remove special characters and get word count of event descriptions
    new_df['event_num_words'] = new_df.description.apply(
        lambda x: len(remove_special_chars(x.split(' '))))

    # replace missing values in duration to median value
    new_df.duration_min.fillna(value=new_df.duration_min.median(), inplace=True)
    # replace missing venue values with 'None'
    new_df.venue.fillna(value='None', inplace=True)
    # replace missing fee values with 'N/A'
    new_df.fee.fillna(value=0, inplace=True)
    # replace missing photo_url values with 'N/A'
    new_df.photo_url.fillna(value=0, inplace=True)

    # extract just the amount from the fee dictionary
    new_df.fee = new_df.fee.apply(lambda x: x['amount'] if x != 0 else 0)

    # encode photo_url column
    new_df['has_photo'] = new_df.photo_url.apply(lambda x: 0 if x == 0 else 1)

    """
    clean the venue column
    """
    # converting the 'venue' column into its own dataframe
    df_venues = new_df['venue'].apply(pd.Series)
    # create list of venue latitude & longitude
    new_df['venue_latlon'] = list(zip(df_venues.lat, df_venues.lon))

    # drop the 'venue' column from df_events
    new_df.drop(columns=['venue', 'why'], inplace=True)

    # rename id column to event_id for clarity
    new_df.rename(index=str, columns={"id": "event_id"})

    return new_df


# function to create engineered features for events data


def engineer_events_features(dataframe):
    """
    This function creates engineered features and outputs an updated dataframe.
    --INPUT--
    Dataframe
    --OUPUT--
    Dataframe
    """

    # convert time to a datetime datatype
    new_df = dataframe
    new_df['time_datetime'] = pd.to_datetime(new_df['time'], unit='ms')
    # adding event date as Year/Month/Day
    new_df['time_m_d_y'] = new_df['time_datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))

    # add column with day of week
    new_df['time_m_d_y'] = pd.to_datetime(new_df['time_m_d_y'])
    new_df['day_of_week'] = new_df['time_m_d_y'].dt.day_name()

    # create column called event_hour - get hour of event
    new_df['event_hour'] = new_df['time_datetime'].dt.hour
    new_df['event_hour'] = new_df['event_hour'].astype('category')

    # bin the event hour into 6 bins (4-hour intervals in 24-day)
    bins = [0, 4, 8, 12, 16, 21, 24]
    new_df['event_hour_group'] = pd.cut(new_df['event_hour'], bins, right=False)

    # add count of subway stations within 0.5 miles from venue
    # load subway station data
    df_subway = pd.read_csv("NYC_Subway_Data.csv")

    # dropping duplicate stations (file contains a location for each entry/exit point which is not what we need)
    df_unique_subway = df_subway.drop_duplicates(subset=["Division", "Station Name"])

    # convert the latitude and longitude into floats for distance calculation
    df_unique_subway['Station Latitude'].astype(float)
    df_unique_subway['Station Longitude'].astype(float)

    # create a new column with the converted latitude and longitutdes in a tuple
    df_unique_subway['latlon'] = list(
        zip(df_unique_subway['Station Latitude'], df_unique_subway['Station Longitude']))

    # create a variable with a list of each station's (latitude, longitude)
    subway_locations = list(df_unique_subway['latlon'])

    # save the subway_locations variable
    with open('subway_locations.pkl', 'wb') as f:
        pickle.dump(subway_locations, f)

    # import function created to get the distances of each venue to each subway station
    # apply/lambda function to every event
    new_df['subway_distances'] = new_df['venue_latlon'].apply(
        lambda x: get_subway_distances(x, subway_locations))

    # create a column with a count of subway stations less than 0.5 miles from each venue
    new_df['num_close_subways'] = new_df['subway_distances'].apply(
        lambda x: len([i for i in x if i <= 0.5]))

    # create new column that notes whether there is a fee or no fee for the event
    new_df['has_fee'] = new_df.fee.apply(lambda x: 0 if x == 0 else 1)

    # get number of days from event creation to event date
    new_df['created_to_event_days'] = (new_df['time'].astype(
        int)-new_df['created'].astype(int))/86400000

    # create dataframe for total number of events held in 2018 by group
    df_num_past_events = pd.DataFrame(new_df.group_id.value_counts()).reset_index()
    df_num_past_events.columns = ['group_id', 'num_past_events']

    # merge multiple dataframes

    # load group dataframe
    df_groups = pd.read_pickle('df_all_groups_cleaned.pickle')
    df_events_group = pd.merge(new_df, df_groups, how='left', on='group_id')
    df_events_group_past = pd.merge(df_events_group, df_num_past_events, how='left', on='group_id')

    # rename columns
    df_events_group_past.rename(columns={'created_x': 'event_created',
                                         'description_x': 'event_description',
                                         'duration_min': 'event_duration',
                                         'headcount': 'event_headcount',
                                         'id': 'event_id',
                                         'name_x': 'event_name',
                                         'rating': 'event_rating',
                                         'status_x': 'event_status',
                                         'time': 'event_time',
                                         'updated': 'event_updated',
                                         'visibility_x': 'event_visibility',
                                         'descrip_tokens': 'event_descrip_tokens',
                                         'descrip_num_words': 'event_descrip_num_words',
                                         'has_fee': 'has_event_fee',
                                         'created_y': 'group_created',
                                         'description_y': 'group_description',
                                         'join_mode': 'group_join_mode',
                                         'lat': 'group_lat',
                                         'lon': 'group_lon',
                                         'link': 'group_link',
                                         'state': 'group_state',
                                         'members': 'num_members',
                                         'name_y': 'group_name',
                                         'status_y': 'group_status',
                                         'urlname': 'group_urlname',
                                         'visibility_y': 'group_visibility',
                                         'who': 'group_who',
                                         'category_name': 'group_category',
                                         'organizer_id': 'group_organizer_id',
                                         'yrs_since_created': 'group_yrs_est',
                                         'created_date': 'group_created_date'
                                         }, inplace=True)
    # save the merged dataframe
    df_events_group_past.to_pickle('df_2018_cleaned.pickle')

    return df_events_group_past
