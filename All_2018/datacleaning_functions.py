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


# function to remove special character tokens in the tokenzied descriptions

def remove_special_chars(some_list):
    remove = ["-", "--", "###", "##", "", "•"]
    return [x for x in some_list if x not in remove]

# function to get distanes to subway stations from each venue


def get_subway_distances(coord, subway_locations):
    """
    returns a list of distances from venue to each subway station in NYC,
    sorted from closest to farthest
    """
    return sorted([haversine(coord, s, unit='mi') for s in subway_locations])
