from django.shortcuts import render
from pathlib import Path
from classifier.forms import SentimentFeatureForm
from classifier.preprocess import MLConfig

# Displays the home view and initialize the forms
def home(request):
    form = SentimentFeatureForm()
    return render(request, 'pages/home.html', {'form': form})

def predict(request):
    """
        Retrieves the input from the form fields and
        passes the inputs to the model for prediction.
    """
    targets = ["Negative", "Neutral", "Positive"]
    context = {}
    if request.method == 'POST':
        form = SentimentFeatureForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            preprocessed_text = MLConfig().preprocess_text(text)
            tfidf = MLConfig().vectorizer.transform([preprocessed_text])
            prediction = MLConfig().model.predict(tfidf)
            estimates = MLConfig().model.predict_proba(tfidf)
            print("HELLLLLLLOOOOOOOOO", type(estimates))
            estimates = estimates.tolist()[0]
            print(estimates[0])
            prediction_probas = [f"{prob*100:.2f}%" for prob in estimates]
            prediction_proba_classes = zip(targets, prediction_probas)

            # Sort the probabilities
            prediction_proba_classes = sorted(prediction_proba_classes, key=lambda x: x[1], reverse=True)
            print(prediction)
            print(prediction_probas)

            context = {
                'form': form,
                'predictions': prediction_proba_classes
            }
    return render(request, 'pages/home.html', context)