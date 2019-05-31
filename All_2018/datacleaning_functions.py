# Helper functions for cleaning all 2018 events data


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
    # convert values in duration column from milliseconds to minutes
    dataframe['duration'] = dataframe['duration'].apply(lambda x: x/60000)
    # label encode value for whether group's join-mode is open or not
    dataframe['group_is_open'] = dataframe.group.apply(
        lambda x: 1 if x['join_mode'] == 'open' else 0)
    # extract group_id from the group column which contains a dictionary of group details
    dataframe['group_id'] = dataframe.group.apply(lambda x: x.get('id'))
    # rename column to note time unit of the data
    dataframe.rename(columns={'duration': 'duration_min'}, inplace=True)
    # fill in NaNs, then label encode
    dataframe['how_to_find_us'].fillna(0, inplace=True)
    dataframe['has_how_to_find'] = dataframe['how_to_find_us'].apply(lambda x: 1 if x != 0 else 0)
    dataframe['rsvp_limit'].fillna(0, inplace=True)
    dataframe['has_rsvp_limit'] = dataframe['rsvp_limit'].apply(lambda x: 1 if x != 0 else 0)
    # fill in Nans, then clean text using regex helper function
    dataframe.description.fillna(value='None', inplace=True)
    dataframe['description'] = dataframe['description'].apply(lambda x: clean_text(x))
    # remove special characters and get word count of event descriptions
    dataframe['event_num_words'] = dataframe.description.apply(
        lambda x: len(remove_special_chars(x.split(' '))))
    # replace missing values in duration to median value
    dataframe.duration_min.fillna(value=dataframe.duration_min.median(), inplace=True)
    # replace missing venue values with 'None'
    dataframe.venue.fillna(value='None', inplace=True)
    # replace missing fee values with 'N/A'
    dataframe.fee.fillna(value=0, inplace=True)
    # replace missing photo_url values with 'N/A'
    dataframe.photo_url.fillna(value=0, inplace=True)
    # extract just the amount from the fee dictionary
    dataframe.fee = dataframe.fee.apply(lambda x: x['amount'] if x != 0 else 0)
    # encode photo_url column
    dataframe['has_photo'] = dataframe.photo_url.apply(lambda x: 0 if x == 0 else 1)

    """
    cleaning the venue column
    """
    # converting the 'venue' column into its own dataframe
    df_venues = dataframe['venue'].apply(pd.Series)
    # create list of venue latitude & longitude
    dataframe['venue_latlon'] = list(zip(df_venues.lat, df_venues.lon))
    # drop the 'venue' column from df_events
    dataframe.drop(columns=['venue'], inplace=True)
    # rename id column to event_id for clarity
    dataframe.rename(index=str, columns={"id": "event_id"})

    return dataframe


# function to remove special character tokens in the tokenzied descriptions

def remove_special_chars(some_list):
    remove = ["-", "--", "###", "##", "", "•"]
    return [x for x in some_list if x not in remove]
