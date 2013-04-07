import Qt 4.7

Rectangle {

    NavigationButtons {
        id: buttonRow
        z: 1
        anchors.top: parent.top
        width: parent.width; height: button_height()
        onButtonClicked: buttonController.buttonClicked(button)
    }

    Flickable {
        id: flickable
        anchors.top: buttonRow.bottom
        width: parent.width
        //contentWidth: parent.width
        contentHeight: 160
        height: 100
        //flickableDirection: Flickable.VerticalFlick
        //clip: true
        //Column {
        //anchors.centerIn: parent

        Rectangle {
            id: one;
            height: 40; width: parent.width;
            color: "#222"
            Text {
                text: "Download more books"
                color: "steelblue"
                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: toolsController.toolsClicked(0)
            }
        }

        //Rectangle { id: two;   anchors.top: one.bottom;   height: 40; width: parent.width; color: "green" }
            //Rectangle { id: three; anchors.top: two.bottom;   height: 40; width: parent.width; color: "blue" }
            //Rectangle { id: four;  anchors.top: three.bottom; height: 40; width: parent.width; color: "yellow" }

        //FtpLogin {
        //    id: one;
        //    onHostTextChanged: console.log("Tools host text changed", hostText)
        //    onPortTextChanged: console.log("Tools got", portText)

        //    hostText: ftpController.host
        //    portText: ftpController.port

        //}
        //FtpLogin { id: two; anchors.top: one.bottom }
            //FtpLogin {  }
        }
    //}
}
