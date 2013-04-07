import Qt 4.7

Rectangle {
    color: "black"
    ScriptBookGradients { id: cg }

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
        contentHeight: 160
        height: 100

        Rectangle {
            id: ftpConnect;
            height: 40; width: parent.width; gradient: cg.onn
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

        Rectangle {
            id: fontSettings;
            height: 40; width: parent.width; gradient: cg.off
            anchors.top: ftpConnect.bottom
            Text {
                text: "Font settings"
                color: "steelblue"
                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: toolsController.toolsClicked(1)
            }
        }

        Rectangle {
            id: bokMarks;
            height: 40; width: parent.width; gradient: cg.onn
            anchors.top: fontSettings.bottom
            Text {
                text: "Bookmarks"
                color: "steelblue"
                anchors.centerIn: parent
            }

            MouseArea {
                anchors.fill: parent
                onClicked: toolsController.toolsClicked(2)
            }
        }

    }
}
