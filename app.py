from flask import Flask, request, render_template, redirect, url_for, session
import pandas as pd
from modules.levenshtein import calculate_levenshtein_distances
from modules.clustering_descriptions import cluster_descriptions

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

projects = None
levenshtein_results = None
clustering_results = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global projects
    if request.method == 'POST':
        file = request.files['file']
        if file:
            projects = pd.read_csv(file)
            session['columns'] = projects.columns.tolist()
            return redirect(url_for('select_columns'))
    return render_template('upload.html')

@app.route('/select_columns', methods=['GET', 'POST'])
def select_columns():
    global projects, levenshtein_results, clustering_results
    columns = session.get('columns', [])
    if request.method == 'POST':
        title_column = request.form['title_column']
        description_column = request.form['description_column']
        if title_column and description_column:
            session['title_column'] = title_column
            session['description_column'] = description_column
            titles = projects[title_column]
            descriptions = projects[description_column]
            levenshtein_results = calculate_levenshtein_distances(titles)
            clustering_results = cluster_descriptions(descriptions)
            return redirect(url_for('project_list'))
    return render_template('select_columns.html', columns=columns)

@app.route('/projects')
def project_list():
    global projects, clustering_results
    title_column = session.get('title_column')

    # Calculate cluster sizes
    cluster_sizes = {}
    for label in clustering_results:
        if label != -1:
            cluster_sizes[label] = cluster_sizes.get(label, 0) + 1

    # Create a list of projects with their cluster sizes
    projects_with_clusters = []
    for index, project in projects.iterrows():
        cluster_label = clustering_results[index]
        cluster_size = cluster_sizes.get(cluster_label, 0) if cluster_label != -1 else 0
        projects_with_clusters.append((project[title_column], cluster_label, cluster_size, index))

    # Sort projects by cluster size (descending) and cluster label
    projects_with_clusters.sort(key=lambda x: (-x[2], x[1]))

    return render_template('project_list.html', projects=projects_with_clusters)

@app.route('/project/<int:project_id>')
def project_details(project_id):
    global projects, levenshtein_results, clustering_results
    title_column = session.get('title_column')
    description_column = session.get('description_column')
    project = projects.iloc[project_id]
    similar_cluster = get_similar_projects_cluster(project_id)
    similar_levenshtein = get_similar_projects_levenshtein(project_id)
    return render_template('project_details.html', project=project, title_column=title_column, description_column=description_column, similar_cluster=similar_cluster, similar_levenshtein=similar_levenshtein)

def get_similar_projects_levenshtein(project_id, threshold=75):
    global projects, levenshtein_results
    title_column = session.get('title_column')
    project_title = projects.iloc[project_id][title_column]
    similar_projects = []
    for (i, j), distance in levenshtein_results.items():
        if i == project_id or j == project_id:
            other_project_id = j if i == project_id else i
            other_project_title = projects.iloc[other_project_id][title_column]
            similarity = 1 - (distance / max(len(project_title), len(other_project_title)))
            if similarity >= threshold / 100:
                similar_projects.append(other_project_title)
    return similar_projects

def get_similar_projects_cluster(project_id):
    global projects, clustering_results
    cluster_id = clustering_results[project_id]
    if cluster_id == -1:
        return []  # No similar projects if the current project is noise
    similar_projects = [projects.iloc[i][session.get('title_column')] for i in range(len(clustering_results)) if clustering_results[i] == cluster_id and i != project_id and clustering_results[i] != -1]
    return similar_projects

if __name__ == '__main__':
    app.run(debug=True)
