const socket = io();

let currentJsonPath = '';

document.getElementById('upload-form').addEventListener('submit', (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('video-file');
    const spinner = document.getElementById('loading-spinner');
    spinner.style.display = 'block';  // Show the spinner

    if (fileInput.files.length === 0) {
        alert('Please select a video file.');
        spinner.style.display = 'none';  // Hide the spinner
        return;
    }

    const formData = new FormData();
    formData.append('video', fileInput.files[0]);

    fetch('/upload_video', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        spinner.style.display = 'none';  // Hide the spinner
        if (data.success) {
            socket.emit('start_video', { video_path: data.video_path });
        } else {
            alert('Failed to upload video.');
        }
    })
    .catch(error => {
        spinner.style.display = 'none';  // Hide the spinner
        console.error('Error:', error);
    });
});

document.getElementById('stop-button').addEventListener('click', (e) => {
    e.preventDefault();
    socket.emit('stop_video');
});

document.getElementById('generate-graphs-button').addEventListener('click', (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('json-file');
    if (fileInput.files.length === 0) {
        alert('Please select a JSON file.');
        return;
    }

    const formData = new FormData();
    formData.append('json', fileInput.files[0]);

    fetch('/upload_json', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentJsonPath = data.json_path;  // Save the current JSON path
            const graphContainer = document.getElementById('graph-container');
            graphContainer.innerHTML = '';  // Clear existing graphs
            data.graphs.forEach(graph => {
                const img = document.createElement('img');
                img.src = `/graphs/${graph}?t=${new Date().getTime()}`;  // Add timestamp to avoid caching
                img.alt = 'Graph';
                graphContainer.appendChild(img);
            });
        } else {
            alert('Failed to upload JSON.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('clear-button').addEventListener('click', (e) => {
    e.preventDefault();
    clearGraphs();
});

document.getElementById('save-csv-button').addEventListener('click', (e) => {
    e.preventDefault();
    saveFile('csv');
});

document.getElementById('save-excel-button').addEventListener('click', (e) => {
    e.preventDefault();
    saveFile('excel');
});

function saveFile(format) {
    const fileInput = document.getElementById('json-file');
    if (fileInput.files.length === 0) {
        alert('Please select a JSON file.');
        return;
    }

    const formData = new FormData();
    formData.append('json', fileInput.files[0]);
    formData.append('format', format);

    fetch('/save_file', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`${format.toUpperCase()} file saved: ${data.path}`);
        } else {
            alert(`Failed to save ${format.toUpperCase()} file.`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function clearGraphs() {
    const graphContainer = document.getElementById('graph-container');
    graphContainer.innerHTML = '';
}

socket.on('frame', (data) => {
    const img = document.getElementById('video-frame');
    img.src = 'data:image/jpeg;base64,' + data.frame;
    img.style.width = '150%';  // Increase size to 150%
});

socket.on('error', (data) => {
    alert(data.message);
    document.getElementById('loading-spinner').style.display = 'none';  // Hide the spinner on error
});

socket.on('saved', (data) => {
    const messageDiv = document.getElementById('message');
    messageDiv.innerText = data.message;
    messageDiv.className = 'alert alert-success';
    document.getElementById('loading-spinner').style.display = 'none';  // Hide the spinner when saved

    const graphContainer = document.getElementById('graph-container');
    graphContainer.innerHTML = '';  // Clear existing graphs
    data.graphs.forEach(graph => {
        const img = document.createElement('img');
        img.src = `/graphs/${graph}?t=${new Date().getTime()}`;  // Add timestamp to avoid caching
        img.alt = 'Graph';
        graphContainer.appendChild(img);
    });
});
