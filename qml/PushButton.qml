import QtQuick 1.0


Rectangle {
    id: button
    radius: 2; height: 50; width: 100;
    border.color: "black"; border.width: 2

    signal trigger
    signal down
    signal up
    signal keyPressed (int key)

    property alias text: buttonText.text
    property alias textColor: buttonText.color
    property alias focusItem: button


    Keys.onPressed: {
        if (event.key == Qt.Key_Return) {
            button.trigger()
            button.keyPressed(event.key)
            event.accepted = true;
        }
        else {
            button.keyPressed(event.key)
        }
    }


    Text { id: buttonText; text: button.text; anchors.centerIn: parent }

    MouseArea {
        id: mouseArea
        anchors.fill: parent;

        /// When mouse button is pressed down
        onPressed: button.down()

        /// When mouse button is released
        onReleased: button.up()

        /// The 'click' behavior
        onClicked: button.trigger()
    }
}
