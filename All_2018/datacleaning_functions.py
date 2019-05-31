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
    This function will perform all data cleaning activities; takes in a
    dataframe as an input.
    --INPUT--
    Dataframe
    --OUTPUT--
    Dataframe
    """
