const timeLabel = document.getElementById('timeString');
const pulsante = document.getElementById('pulsante');
const latitudeTag = document.getElementById('latitude');
const longitudeTag = document.getElementById('longitude');

let startMode = true; // Impostiamo startMode a true per avviare il timer all'inizio
let timerInterval;
var seconds = 0;
var minutes = 0;
var hours   = 0;
const positionList = [];
download_file_name = ''

function buttonClick() {
    startMode = !startMode;
    // Cambiamo il nome al pulsante
    if (startMode) {
        pulsante.innerHTML = "START";
        clearInterval(timerInterval);
        reset();
    } else {
        document.getElementById("download-button").style.display = "none"
        pulsante.innerHTML = "STOP";
        timerInterval = setInterval(startTime, 1000); // Aggiorniamo il tempo ogni secondo
    }
}


function startTime() {
    //TimeFormat
    seconds += 1;
    minutes = parseInt(seconds / 60);
    hours   = parseInt(minutes / 60);
    const timeString = `${hours}:${minutes % 60}:${seconds % 60}`;
    timeLabel.innerHTML = timeString;


    if('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(position => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            /*const altitude = position.coords.altitude;
            console.log("altitude" + altitude)
            const timestamp = new Date(position.timestamp);
            console.log("Time stamp" + timestamp)*/

             /* Ottieni l'ora e la data formattate
             const hours = timestamp.getHours().toString().padStart(2, '0');
             const minutes = timestamp.getMinutes().toString().padStart(2, '0');
             const seconds = timestamp.getSeconds().toString().padStart(2, '0');
            */

             // Update HTML elements with the coordinates and altitude
            latitudeTag.innerHTML = latitude;
            longitudeTag.innerHTML = longitude;

            
            positionList.push({ latitude, longitude/*, altitude, timestamp */});
        });
    }
    
}

function reset(){
    sendPositionListToServer();

    seconds = 0
    minutes = 0
    hours   = 0
    const timeString = `${hours}:${minutes % 60}:${seconds % 60}`;
    timeLabel.innerHTML = timeString;

    latitudeTag.innerHTML = '';
    longitudeTag.innerHTML = '';



}

function sendPositionListToServer() {
    console.log(positionList);
    // Converti la lista in formato JSON
    const jsonData = JSON.stringify({"positions":positionList});
    console.log(jsonData);

    positionList.length = 0;


    // Imposta le opzioni della richiesta
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonData
    };

    // Execute the POST request to the FastAPI server
    fetch('http://127.0.0.1:8000/upload', requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore nella richiesta al server');
            }
            return response.json();
        })
        .then(data => {
            download_file_name = data.filename
            document.getElementById("download-button").style.display = "inline"
        })
        .catch(error => {
            console.error('Errore durante la richiesta al server:', error);
        });


}

document.getElementById('download-button').addEventListener('click', async () => {

    const link = document.createElement('a');
    link.href = `http://127.0.0.1:8000/download/${download_file_name}`;
    link.download = download_file_name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});
