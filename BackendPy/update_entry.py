def entry(plate):
    from firebase import firebase
    from datetime import datetime
    firebase = firebase.FirebaseApplication('https://anpr-265503.firebaseio.com/', None)
    now = datetime.now()
    # plate = "MH03BE8760"  # idhar baadmae current plate okok
    current_time = now.strftime("%m/%d/%y %H:%M:%S")
    print(current_time)
    firebase.put('/Cars/' + plate, "Entry Time", current_time)
    Uid = firebase.get('/Cars', plate + "/uid")
    data = firebase.get('/Cars', plate)
    entry_time = datetime.strptime(firebase.get('/Cars/' + plate, 'Entry Time'), "%m/%d/%y %H:%M:%S")
    firebase.put('user-posts', Uid + "/Recent/" + plate+" " + str(entry_time), data)
    firebase.put('user-posts', Uid + "/History/" + plate+" " + str(entry_time), data)
    # print('Entry Record Updated')


if __name__ == "__main__":
    # entry("DL7CQ1939")
    entry("QWE")