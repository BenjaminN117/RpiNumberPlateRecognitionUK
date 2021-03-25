import base64
import json
import ssl
import http.client as httplib # Python 3
import cv2
import imutils
import requests


def Sighthound(): # Executes the sighthound API and finds the exact number plate characters / This also checks the plate against a database
    headers = {"Content-type": "application/json",
    "X-Access-Token": "ENTER SIGHTHOUND TOKEN HERE"}
    conn = httplib.HTTPSConnection("dev.sighthoundapi.com",
    context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))

    # To use a hosted image uncomment the following line and update the URL
    #image_data = "http://example.com/path/to/hosted/image.jpg"

    # To use a local file uncomment the following line and update the path
    image_data = base64.b64encode(open("1.jpg", "rb").read()).decode() #Encodes the image and sends it to Sighthound

    params = json.dumps({"image": image_data})
    conn.request("POST", "/v1/recognition?objectType=licenseplate", params, headers)
    response = conn.getresponse()
    result = response.read()

    manip = str(result)

    print("Detection Results = " + str(result))


    file = open("NumberPlates.txt", ("r")) # Open the Numberplates file
    lines = []
    for line in file: # Clone the list into a local array
        lines.append(line[:len(line) - 1])
    file.close()
    print(lines) #DEBUG

    #print(manip.find("")) #DEBUG

    plate = manip[317], manip[318], manip [319], manip[320], manip[321], manip[322], manip[323] #Concatenate the letters to a list

    def listToString(plate): #Compile the list into a string
        # initialize an empty string
        str1 = ""

        # traverse in the string
        for ele in plate:
            str1 += ele

            # return string
        return str1

    print(listToString(plate)) #DEBUG

    if listToString(plate) in lines: # Compare the string with the text file of number plates
        print("Found")
        print("Sending commands to IFTTT")
        IFTTT_url = 'ENTER IFTTT URL + TOKEN HERE'
        x = requests.post(IFTTT_url)

    else:
        print("Not found")


# CV2 plate detection, only detects if there is a number plate in the image
def plate_detection():
    img = cv2.imread('1.jpg', cv2.IMREAD_COLOR)

    img = cv2.resize(img, (620, 480))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
    edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection

    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        print("No number plate detected")
        #
    else:
        print("Found a number plate!!")
        print("Sending to Sight Hound")
        Sighthound()

#Image triggering goes here

plate_detection()
