from flask import Flask, request, render_template
import pickle
import pandas as pd
import datetime
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.preprocessing import label_binarize, normalize
from xgboost import XGBClassifier
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    if request.method == 'POST':

        # load existing dataframe to pull group info faster
        df = pd.read_pickle('df_2018_cleaned.pickle')
        df['is_tech'] = df['group_category'].apply(lambda x: 1 if x == 'tech' else 0)

        try:
            group_info = dict(df[df['group_name'] == request.form['group_name']].iloc[0])
        except:
            return "Invalid group name or missing information."

        # format event_hour_group
        event_hour = datetime.datetime.strptime(request.form['start_time'], '%H:%M').hour
        # event_hour = request.form['start_time'].hour

        # format created_to_event_days
        days_between = int(datetime.datetime.strptime(
            request.form['event_date'], '%Y-%m-%d').strftime('%s')) - int(datetime.datetime.today().strftime('%s'))
        days_between = days_between/86400

        # get day of week of the event
        day_of_week = datetime.datetime.strptime(
            request.form['event_date'], '%Y-%m-%d').weekday()

        # get event description word count
        def remove_chars(list_):
            remove = ["-", "--", "###", "##", "", "•"]
            return [x for x in list_ if x not in remove]

        wordcount = len(remove_chars(request.form['description'].split(' ')))

        # create a dictionary with the input values
        input_values = {'event_duration': request.form['duration'],
                        'event_num_words': wordcount,
                        'num_members': group_info.get('num_members'),
                        'group_yrs_est': group_info.get('group_yrs_est'),
                        'num_past_events': group_info.get('num_past_events'),
                        'created_to_event_days': days_between,
                        'group_is_open': group_info.get('group_is_open'),
                        'has_event_fee': request.form['fee'],
                        'day_of_week_Monday': 0,
                        'day_of_week_Saturday': 0,
                        'day_of_week_Sunday': 0,
                        'day_of_week_Thursday': 0,
                        'day_of_week_Tuesday': 0,
                        'day_of_week_Wednesday': 0,
                        'event_hour_group_(4, 8)': 0,
                        'event_hour_group_(8, 12)': 0,
                        'event_hour_group_(12, 16)': 0,
                        'event_hour_group_(16, 21)': 0,
                        'event_hour_group_(21, 24)': 0,
                        'is_tech': group_info.get('is_tech')
                        }

        df_input = pd.DataFrame({k: [v] for k, v in input_values.items()})

        if event_hour < 4:
            pass
        elif event_hour < 8:
            df_input['event_hour_group_(4, 8)'] += 1
        elif event_hour < 12:
            df_input['event_hour_group_(8, 12)'] += 1
        elif event_hour < 16:
            df_input['event_hour_group_(12, 16)'] += 1
        elif event_hour < 21:
            df_input['event_hour_group_(16, 21)'] += 1
        else:
            df_input['event_hour_group_(21, 24)'] += 1

        if day_of_week == 0:
            df_input['day_of_week_Monday'] += 1
        elif day_of_week == 1:
            df_input['day_of_week_Tuesday'] += 1
        elif day_of_week == 3:
            df_input['day_of_week_Thursday'] += 1
        elif day_of_week == 2:
            df_input['day_of_week_Wednesday'] += 1
        elif day_of_week == 5:
            df_input['day_of_week_Saturday'] += 1
        else:
            df_input['day_of_week_Sunday'] += 1

        # normalize the features
        df_scaled = pd.DataFrame(normalize(df_input), columns=df_input.columns)

        # load the trained model
        with open('xgbsmoteenn_model_webapp.pickle', 'rb') as f:
            model = pickle.load(f)

        # make prediction
        label_prediction = model.predict(df_scaled)[0]

        if label_prediction == 1:
            prediction = "1-10"
        elif label_prediction == 2:
            prediction = "11-20"
        elif label_prediction == 3:
            prediction = "21-40"
        elif label_prediction == 4:
            prediction = "41-70"
        elif label_prediction == 5:
            prediction = "71-100"
        else:
            prediction = "101-200"

        my_prediction = f'Approximately {prediction} yes-RSVPs expected.'

        return render_template('result.html', prediction=my_prediction)


if __name__ == '__main__':
    app.run(debug=True)
