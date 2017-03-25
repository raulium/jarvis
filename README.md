# jarvis 2.0
personal home automation solution

## TODO LIST

### Deploy to Apache
* Make applicaiton WSGI compliant, and deploy to Apache
   * [Instructions Here](http://csparpa.github.io/blog/2013/03/how-to-deploy-flask-applications-to-apache-webserver.html)

### Feature List
* Vacation Mode
* Away Mode
* Texting & external messaging
   * Emergency Contact
   * Call-out Sick
   * Deadman's Switch
* Outerwear recommendations based on temperature and weather conditions
* Calendar integration
* Harnascian holidays
* location services
* option to go to bed early
* option to wake up earlier than normal
* Mobile integration
   * side-load phone app
   * transfer functions to laptop while on travel
* lock screen

### Boring Stuff
* Documentation
* Comment the code!
* clean up files
* better logging
* functions should test inputs

### Broken Stuff
* Start Radio function (weblib) doesn't work
* Fix speech system
   * If we play sound files each time, this could prevent Python from moving on before the sound is done playing. Rather than having to sleep each time after 'say'
   * OR, we could sleep for a length determined by the sound file... somehow... like in BIT.

## Dependencies
* google-api-python-client
* speech_recognition
* subprocess
* time
* random
* BeautifulSoup
* urllib
* Flask
