def exit(plate):
    from firebase import firebase
    from datetime import datetime

    now = datetime.now()

    current_time = now.strftime("%m/%d/%y %H:%M:%S")
    curr = datetime.strptime(current_time, "%m/%d/%y %H:%M:%S")
    # maine entry time uuthaya ya pe
    firebase = firebase.FirebaseApplication('https://anpr-265503.firebaseio.com/', None)
    # plate = "MH03BE8760"  # idhar baadmae current plate okok
    entry_time = datetime.strptime(firebase.get('/Cars/' + plate, 'Entry Time'), "%m/%d/%y %H:%M:%S")
    # calculating paise
    diffTime = str(curr - entry_time)
    if len(diffTime) < 8:
        diffTime = "0" + diffTime
    # if else agar unpaid hai toh aage continue nako.
    print(diffTime)
    hr = int(diffTime[0:1]) * 60
    min = int(diffTime[3:5])
    cost = (hr + min) * 100
    # update saare tables
    firebase.put('/Cars/' + plate, "Exit Time", current_time)
    firebase.put('/Cars/' + plate, "Cost", cost)
    firebase.put('/Cars/' + plate, "Parking_time", diffTime)
    firebase.put('/Cars/' + plate, "Status", "Unpaid")
    Uid = firebase.get('/Cars', plate + "/uid")
    data = firebase.get('/Cars', plate)
    print("entry: - ", entry_time)
    firebase.put('user-posts', Uid + "/History/" + plate + " " + str(entry_time), data)
    firebase.delete("user-posts/" + Uid + "/Recent/" + plate+" " + str(entry_time), None)
    # print(help(datetime))
    # print('Exit Record Updated')


if __name__ == "__main__":
    exit("DL7CQ1939")
    # exit("QWE")
    print("hello")