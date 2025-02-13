from scraper import * 
import numpy as np
import datetime

def arrows_to_multiplier(arrows):
    if arrows in ["↗", "↑"]:
        return 1.0
    elif arrows in ["↘", "↓"]:
        return -1.0
    else:
        return 0.0

def generate_predictions(steps=5):
    times = []
    values = []
    arrows = []
    predicted_times = []

    times, values, arrows = scrape()

    def predict(values, arrows, steps):
        values = values[::-1]
        arrows = arrows[::-1]
        multipliers = np.array([arrows_to_multiplier(arrow) for arrow in arrows])
        differences = np.diff(values)
        arrow_effects = differences * multipliers[:-1]
        time = datetime.datetime.now()

        avg_effect = np.mean(arrow_effects[arrow_effects != 0])

        last_value = values[-1]
        predictions = []

        for _ in range(steps):
            next_value = last_value + avg_effect
            predictions.append(next_value.round(1))
            predicted_time = time + datetime.timedelta(minutes=(_ + 1) * 5)
            formated_time = predicted_time.strftime('%H:%M')  
            predicted_times.append(formated_time)
            last_value = next_value
        
        return predictions

    def predict_with_downward_trend(values, steps):
        values = values[::-1]
        last_value = values[-1]
        avg_downward_effect = -np.abs(np.mean(np.diff(values)))

        predictions = []

        for _ in range(steps):
            next_value = last_value + avg_downward_effect
            predictions.append(next_value.round(1))
            last_value = next_value
        
        return predictions

    predictions = predict(values, arrows, steps)
    predictions_downward = predict_with_downward_trend(values, steps)
    
    return predictions, predictions_downward, predicted_times
