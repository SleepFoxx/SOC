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

def generate_predictions(steps=6):
    times = []
    values = []
    arrows = []
    predicted_times = []

    times, values, arrows = scrape()

    def predict(values, arrows, steps):
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
        
        float_predictions = [float(pred) for pred in predictions]
        return float_predictions

    predictions = predict(values, arrows, steps)
    
    return predictions, predicted_times
print(generate_predictions(5))