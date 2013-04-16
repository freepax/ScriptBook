import QtQuick 1.0


Item {

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
        model: bookListModel
        width: parent.width; height: parent.height - buttonRow.button_height()
        anchors.top: buttonRow.bottom

        delegate: Component {

            Rectangle {
                width: pythonList.width; height: nameText.paintedHeight + 40; color: "steelblue"

                Rectangle {
                    id: bookRect
                    color: index % 2 ? "#111" : "#222"
                    border.color: "black"; border.width: 2
                    width: parent.width; height: nameText.paintedHeight + 40; radius: 6

                    Text {
                        id: entryText
                        text: "Book " + model.bookItem.entry + "    (" + model.bookItem.chapters + " chapters)"
                        color: "steelblue"
                        width: parent.width - 10; height: 30
                        font.pointSize: 10
                        anchors { horizontalCenter: parent.horizontalCenter; top: parent.top; }
                    }

                    Text {
                        id: nameText
                        wrapMode: Text.Wrap
                        text: model.bookItem.name
                        color: "white"
                        width: parent.width - 10
                        font.pointSize: 10
                        anchors { horizontalCenter: parent.horizontalCenter; top: entryText.bottom }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            controller.clicked(bookListModel, model.bookItem)
                            buttonController.buttonClicked(2)
                        }
                    }
                }
            }
        }
    }

}
