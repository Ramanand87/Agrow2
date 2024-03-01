function record(inputField) {
    try {
        var recognition = new webkitSpeechRecognition() || new SpeechRecognition();
        recognition.lang = "en-US";

        recognition.onresult = function(event) {
            inputField.value = event.results[0][0].transcript;
        }

        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
        }

        recognition.start();
    } catch (error) {
        console.error('Speech recognition not supported or an error occurred:', error);
    }
}
