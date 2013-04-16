import QtQuick 1.0


Item {
    id: root

    NavigationButtons {
        id: buttonRow
        z: 1
        anchors.top: parent.top
        width: parent.width; height: button_height()
        onButtonClicked: buttonController.buttonClicked(button)
        buttonNumber: buttonController.gradient
    }

    ListView {
        id: pythonList
        model: documentListModel
        width: parent.width; height: parent.height - buttonRow.button_height()
        anchors.top: buttonRow.bottom

        delegate: Component {

            Rectangle {
                id: listrect
                width: pythonList.width; height: documentText.paintedHeight + 40; color: "steelblue"

                Rectangle {
                    id: versrect
                    color: index % 2 ? "#111" : "#222"
                    border.color: "black"; border.width: 2
                    width: parent.width; height: documentText.paintedHeight + 40; radius: 6

                    Text {
                        id: fileSizeText
                        text: "Entry " + model.documentItem.entry + "  Size  " + model.documentItem.filesize
                        color: "steelblue"
                        width: parent.width - 10; height: 30
                        font.pointSize: 11
                        anchors { horizontalCenter: parent.horizontalCenter; top: parent.top; }
                    }

                    Text {
                        id: documentText
                        text: model.documentItem.filename
                        color: "white"
                        width: parent.width - 10
                        font.pointSize: 14
                        wrapMode: Text.Wrap
                        anchors { horizontalCenter: parent.horizontalCenter; top: fileSizeText.bottom }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: { controller.clicked(documentListModel, model.documentItem) }
                    }
                }
            }
        }
    }
}
