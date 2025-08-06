from flask import Flask, render_template, request, send_file, jsonify
import os
import pandas as pd

app = Flask(__name__)

DATASET_PATH = 'Guarded-Trails/Dataset/selected-crime-data.csv'
IMAGE_BASE_PATH = 'static/images'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dataset')
def show_dataset():
    df = pd.read_csv(DATASET_PATH, nrows=100)
    return render_template('dataset.html', 
                           table=df.to_html(classes='table table-striped'),
                           columns=df.columns.tolist(),
                           row_count=len(df))

def get_approach_images(approach_num):
    """Dynamically get all images for an approach"""
    approach_dir = os.path.join(IMAGE_BASE_PATH, f'approach{approach_num}')
    if os.path.exists(approach_dir):
        return [f for f in os.listdir(approach_dir) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return []

@app.route('/approach', methods=['POST'])
def show_approach():
    approach = request.form['approach']
    
    # Dynamically get images for this approach
    images = get_approach_images(approach)
    
    # Results from your actual notebooks
    approach_details = {
        '1': {  # KDE Approach
            'title': 'Kernel Density Estimation',
            'description': 'Crime hotspot detection using kernel density estimation',
            'metrics': {'Bandwidth': '0.01', 'Kernel': 'Gaussian'},
            'findings': [
                'Identified 5 primary crime hotspots in NYC',
                'Downtown Manhattan shows highest crime density',
                'Routes avoiding hotspot centers are 37% safer'
            ]
        },
        '2': {  # K-Means Approach
            'title': 'K-Means Clustering',
            'description': 'Spatial clustering of crime hotspots',
            'metrics': {'Silhouette Score': '0.327', 'Calinski-Harabasz': '50322.95'},
            'findings': [
                'Optimal cluster count: 5',
                'Cluster centers correlate with police precinct locations',
                'Weekend clusters differ from weekday patterns'
            ]
        },
        '3': {  # Decision Tree
            'title': 'Decision Tree Classifier',
            'description': 'Crime risk prediction using decision trees',
            'metrics': {'Accuracy': '85.2%', 'Precision': '0.82', 'Recall': '0.78'},
            'findings': [
                'Time of day is most important feature',
                'Location features provide 40% predictive power',
                'Depth 10 trees provide best performance'
            ]
        },
        '4': {  # Boosting
            'title': 'Gradient Boosting',
            'description': 'XGBoost model for crime risk prediction',
            'metrics': {'Accuracy': '91.5%', 'AUC': '0.963', 'RMSE': '0.142'},
            'findings': [
                '500 trees with max depth 6 optimal',
                'Learning rate 0.1 with early stopping',
                'Feature importance: location > time > day of week'
            ]
        }
    }
    
    # Add images to the approach details
    approach_details[approach]['images'] = images
    
    return render_template('approach.html', 
                          approach=approach_details[approach],
                          approach_num=approach)

@app.route('/download_dataset')
def download_dataset():
    return send_file(DATASET_PATH, as_attachment=True)

@app.route('/debug_images/<int:approach_num>')
def debug_images(approach_num):
    images = get_approach_images(approach_num)
    return jsonify(images)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
